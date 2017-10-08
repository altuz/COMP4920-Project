from backend.models import User, UserSerializer, Register, GameList, PlayerLibrary, Session, Follow, Categories, Rating, Genres
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from hashlib import blake2b
from django.db.models import Q
from functools import reduce
from django.db.models import Count
import smtplib
import json
import time
import operator

# Retrieves user profile along with game list and wish list
# TESTED
@api_view(['GET'])
def user_prof(request):
    game_list = ""
    wish_list = ""
    user_prof = ""
    # Get user
    try:
        user_entry = User.objects.get(user_name = request.GET['username'])
        user_prof = '''
            {{ 
                "username" : "{}",
                "user_id" : "{}"
            }}
        '''.format(user_entry.user_name, user_entry.user_id)
    except:
        HttpResponse('{ "user" : {}, "gamelist" : {}, "wishlist" : {} }')
    # Get game list
    try:
        game_list = get_list(request.GET['username'], True)
    except:
        print("No games")
    # Get wish list
    try:
        wish_list = get_list(request.GET['username'], False)
    except:
        print("No wishes")

    ret_json = '''
        {{
            "user" : "{}",
            "gamelist" : [{}],
            "wishlist" : [{}]
        }}
    '''.format(request.GET['username'], game_list, wish_list)
    return HttpResponse(ret_json)


# Follow user
# User1 -> User2
@api_view(['POST'])
def follow_user(request):
    json_obj = None
    # decond json
    try:
        json_obj = json.loads(request.body.decode())
    except:
        print("Error loading json")
        return HttpResponse('{"message" : "input invalid", "success" : "False"}')
    # check if user1 and user2 exists
    try:
        user_1 = User.objects.get(json_obj['user']['user1'])
        user_2 = User.objects.get(json_obj['user']['user2'])
        new_entry = Follow(user_id = user_1, following = user_2)
        new_entry.save()
        return HttpResponse('{"message" : "Followed", "success" : "True"}')
    except:
        return HttpResponse('{"message" : "User1 or User2 does not exist", "success" : "False"}')


# Helper function for get game/wishlist
# TESTED
def get_list(username, type):
    # retrieve database objects
    try:
        # check if player exist
        # find gamelist related to player
        player = User.objects.get(user_name = username)
        gamelist = None
        if type is True:
            gamelist = PlayerLibrary.objects.filter(user_id=player, played=True)
        else:
            gamelist = PlayerLibrary.objects.filter(user_id=player, played=False, wish_list=True)
        json_list = []
        print(gamelist)
        # convert to json list
        for entries in gamelist:
            try:
                game = entries.game_id
                g_id = game.game_id
                g_name = game.game_name
                g_json = '{{"game_name":"{}", "game_id":"{}"}}'.format(g_name, g_id)
                json_list.append(g_json)
            except:
                continue
        print(','.join(json_list))
        return ','.join(json_list)
    except Exception as e:
        print(e)
        raise e


# Get a user's game list
# TESTED
@api_view(['POST'])
def get_gamelist(request):
    json_obj = None
    # decode json
    try:
        json_obj = json.loads(request.body.decode())
    except:
        print("Error when loading the Json")
        return HttpResponse('{"message":"input invalid", "gamelist":[]}')
    # retrieve database objects
    try:
        # check if player exist
        # find gamelist related to player
        game_list = get_list(json_obj['user']['username'], True)
        # construct json object
        ret_json = '''
            {{
                "message":"success",
                "gamelist": [
                    {}
                ]
            }}
        '''.format(game_list)
        return HttpResponse(ret_json)
    except:
        return HttpResponse('{"message":"does not exist, "gamelist":[]"}')


# Get a user's wish list
# TESTED
@api_view(['POST'])
def get_wishlist(request):
    json_obj = None
    # decode json
    try:
        json_obj = json.loads(request.body.decode())
    except:
        print("Error when loading the Json")
        return HttpResponse('{"message":"input invalid", "wishlist":[]}')
    # retrieve database objects
    try:
        # check if player exist
        # find gamelist related to player
        game_list = get_list(json_obj['user']['username'], False)
        # construct json object
        ret_json = '''
            {{
                "message":"success",
                "wishlist": [
                    {}
                ]
            }}
        '''.format(game_list)
        return HttpResponse(ret_json)
    except:
        return HttpResponse('{"message":"does not exist, "wishlist":[]"}')

# Check if in users game list as played and/or wishlist
# Testing code: Has sample url to test
# curl -X GET "http://localhost:8000/backend/check_in_userlist/?userid=76561197960530222&gameid=578080&played=true&wishlist=false"
@api_view(['GET'])
def check_in_userlist(request):
    try:
        user_id = int(request.GET.get('userid'))
        game_id = int(request.GET.get('gameid'))
        played = (request.GET.get('played') == "true")
        wish_list = (request.GET.get('wishlist') == "true")

        test = PlayerLibrary.objects.get(user_id=user_id,
                                  game_id=game_id,
                                  played=played,
                                  wish_list=wish_list)
        return HttpResponse('{"message":"Success"}')
    except:
        return HttpResponse('{"message":"Invalid Request"}')


# Adding a game to a user's wish or played list
# TESTED
@api_view(['POST'])
def edit_list(request):
    json_obj = None
    try:
        json_obj = json.loads(request.body.decode())
    except:
        print("Error when loading the Json")
        return HttpResponse('{"message":"input invalid", "gamelist":{}}')

    try:
        # Checks if player exist in database
        # Checks if game exist in database
        # Unsuccessful if either check throws does not exist
        player  = User.objects.get(user_name = json_obj['user']['userid'])
        game    = GameList.objects.get(game_id = json_obj['user']['gameid'])
        played  = json_obj['user']['played']
        wishes  = json_obj['user']['wish']
        new_entry = PlayerLibrary(user_id = player, game_id = game, wish_list = wishes, played = played)
        new_entry.save()
        return HttpResponse('''
            {
                "message":"Successful"
            }    
        ''')
    except:
        return HttpResponse('''
            {
                "message":"Invalid Request"
            }
        ''')


# curl -d "param1=value1&param2=value2" -X POST http://localhost:3000/data
@api_view(['POST'])
# TESTED
def login(request):
    obj = None
    user_entry = None
    #Check if user is activated
    try:
        obj = json.loads(request.body.decode())
        print(obj)
    except:
        print("Error when loading the Json")
        return HttpResponse('{"message":"input invalid", "user":{}}')

    try:
        user_entry = Register.objects.get(user_name = obj['user']['username'])
        # If it doesn't throw exception, user has not activated
        return HttpResponse('{"message":"account not activated", "user":{}}')
    except:
        try:
            user_entry = User.objects.get(user_name=obj['user']['username'],
                                            pass_word=obj['user']['password'])
        except:
            return HttpResponse('{"message":"does not exist", "user":{}}')

    # Initialise values
    game_list = ""
    wish_list = ""
    # Get game list
    try:
        game_list = get_list(obj['user']['username'], True)
    except:
        print("No games")
    # Get wish list
    try:
        wish_list = get_list(obj['user']['username'], False)
    except:
        print("No wishes")

    # Session
    # user_id
    # session_id
    # Get time and hash.
    # Insert it as session
    user_dict = user_entry.as_dict()
    user_session = blake2b(str(time.time()).encode('utf-8')).hexdigest()
    # response.set_cookie('session_id', user_session);
    # response.set_cookie('username', obj['user']['username'])
    ret_json = '''
        {{
            "message" : "success",
            "user" : {{
                "user_name" : "{}",
                "email" : "{}"
            }},
            "cookie" : {{
                "user_name" : "{}",
                "session" : "{}"
            }},
            "gamelist" : [{}],
            "wishlist" : [{}]
        }}
    '''.format(user_dict['user_name'], user_dict['email'], user_dict['user_name'], user_session, game_list, wish_list)
    new_session = Session(user_id = user_entry, session_id = user_session)
    new_session.save()
    response = HttpResponse(ret_json)
    return response


@api_view(['POST'])
# TESTED
def session_check(request):
    json_obj = None
    # decode json
    try:
        json_obj = json.loads(request.body.decode())
    except:
        print("Error when loading the Json")
        return HttpResponse('{"message":"input invalid, "user":{}"}')

    try:
        user_entry = User.objects.get(user_name = json_obj['user']['username'])
        session_entry = Session.objects.get(user_id = user_entry, session_id = json_obj['user']['session_id'])
        user_dict = user_entry.as_dict()
        response = '''
                {{
                    "message" : "success",
                    "user" : {{
                        "user_name" : "{}",
                        "email" : "{}"
                    }},
                }}
        '''.format(user_dict['user_name'], user_dict['email'])
        return HttpResponse(response)
    except:
        return HttpResponse('{"message":"does not exist or session invalid", "user":{}}')

@api_view(['POST'])
# TESTED
def logout(request):
    response = HttpResponse('{"message":"success"}')
    response.delete_cookie('session_id')
    response.delete_cookie('username')
    json_obj = None
    # decode json
    try:
        json_obj = json.loads(request.body.decode())
    except:
        print("Error when loading the Json")
        return HttpResponse('{"message":"input invalid, "user":{}"}')

    try:
        user_entry = User.objects.get(user_name = json_obj['user']['username'])
        session_entry = Session.objects.get(user_id = user_entry, session_id = json_obj['user']['session_id'])
        session_entry.delete()
    except:
        return HttpResponse('{"message":"does not exist or session invalid", "user":{}}')

    return response


def objs_to_json(objs):
    serializer = UserSerializer(objs)
    decoded_str = JSONRenderer().render(serializer.data).decode()
    return msg_with_data(decoded_str)


def msg_with_data(json_obj):
    return '{"message":"success", "user":%s}' % json_obj


def msg_to_json(msg):
    return '{"message":"%s"}' % msg


# user Registration
@api_view(['POST'])
def register(request):
    """
    post method function, get user information and put him in register table
    :param request: the request object
    :return: different json object represent different info
    """
    print("user sign up function is running ...")
    print("")
    obj = None
    try:
        obj = json.loads(request.body.decode())
    except:
        print("Error when loading the Json")
        pass

    if obj is not None:
        # check user existence
        try:
            exist_user = User.objects.get(user_name=obj['user']['user_name'])
        #print(exist_user)
            return HttpResponse(msg_to_json("user already exist"))
        except:
            # create new user for the register table and get info from the request
            user_name=obj['user']['user_name']
            password = obj['user']['pass_word']
            key = blake2b((user_name + password).encode('utf-8')).hexdigest()  # key send to the user
            link = "http://localhost:8090/activate/" + key

            # send activation email
            try:
                server = smtplib.SMTP('smtp.gmail.com:587')
                server.starttls()
                server.login('yun553966858@gmail.com', 'asdqwienvlasdkf')
                message = 'Subject: {}\n\n{}'.format("SteamR Registration",
                                                 "User Name: %s\nActivation Link: %s\n" % (obj['user']['user_name'], link))
                server.sendmail('SteamR Team', obj['user']['email'], message)
                server.quit()
            except smtplib.SMTPException:
                return HttpResponse(msg_to_json("fail to send email"))

            new_register = Register(user_name=obj['user']['user_name'], email=obj['user']['email'],
                                pass_word=obj['user']['pass_word'], privacy=obj['user']['privacy'], key=key)
            new_register.save()
            print(new_register)
            return HttpResponse(msg_to_json("register created successfully"))
    else:
        return HttpResponse(msg_to_json("json loading failed"))


# activate user, put user into user table
@api_view(['GET'])
def activate(request, key):
    """
    function that try to sign up a registered user (activate a user)
    :param request:
    :param key: activation key
    :return: if activation key exist create the user account in the table and return true, else return json no exist
    """
    try:
        exist_register = Register.objects.get(key=request.GET['key'])


         # create the new user
        new_user = User(user_name=exist_register.user_name, email=exist_register.email,
                    pass_word=exist_register.pass_word, privacy=exist_register.privacy)
        new_user.save()

        # delete entry in the register table
        exist_register.delete()
    
        return HttpResponse(msg_to_json("used activated"))
    except:
        return HttpResponse(msg_to_json("request failed"))


# Search for games
# For testing - note: %20 is a space, %2C is a comma in URL character encoding
# curl -X GET "http://localhost:8000/backend/search_game/?q=for%20left&category=strategy%2CRTS"
# curl -X GET "http://localhost:8000/backend/search_game/?q=soldier&category=Multi%2DPlayer"
# curl -X GET "http://localhost:8000/backend/search_game/?q=&category=Multi%2DPlayer%2CCo%2Dop&genre=Action%2CAdventure"
@api_view(['GET'])
def search_game(request):
    """
    function that searches for games matching search criteria
    :param request: the search request with parameters q=keywords_separated_by_spaces, category=categories_separated_by_commas
    :return: if search match, return match list, else return empty JSON object
    """
    print("search game function is running ...")
    print("")
    # TODO check if try-catch is slow
    # try:
    query = request.GET.get('q')
    category = request.GET.get('category')
    genre = request.GET.get('genre')

    # Step 1: Filter by keyword
    if query:
        query_list = query.split(" ")
        results = GameList.objects.filter(
            reduce(operator.and_,(Q(game_name__icontains=q) for q in query_list))
        )# Returns a QuerySet
    else:
        results = GameList.objects.all() # Return all the results if no key words are given

    # Step 2: Filter by category
    if category:
        category_list = category.split(",")
        catObjsUnion = Categories.objects.filter(reduce(operator.or_, (Q(category__iexact=c) for c in category_list)))
        catObjs = catObjsUnion.values('game_id').annotate(matches=Count('game_id')) # Count subquery matches and assign a 'mathes' column to store count
        catObjs = catObjs.filter(matches__exact=len(category_list)) # Filter to get ONLY games that match ALL given category tags

        results = results.filter(game_id__in=catObjs.values('game_id')) # Filter previous results from previous filter

    # Step 3: Filter by genre
    # TODO need to test more, for multiply genres
    if genre:
        genre_list = genre.split(",")
        genreObjsUnion = Genres.objects.filter(reduce(operator.or_, (Q(genre__iexact=g) for g in genre_list)))
        genreObjs = genreObjsUnion.values('game_id').annotate(matches=Count('game_id')) # Count subquery matches and assign a 'mathes' column to store count
        genreObjs = genreObjs.filter(matches__exact=len(genre_list)) # Filter to get ONLY games that match ALL given genre tags

        results = results.filter(game_id__in=genreObjs.values('game_id'))  # Filter previous results from previous filter

    # Put 'results' querySet into dict format to convert into JSON dict
    results_list = [obj.as_dict() for obj in results]
    outputJSON = json.dumps({"results": results_list},ensure_ascii=False).encode('utf16')
    return HttpResponse(outputJSON, content_type='application/json')
    # except:
    #     return HttpResponse('{"message":"input invalid", "search-games":{}}')

# Get the top "n" number of games
# curl -X GET "http://localhost:8000/backend/get_top_games/?n=100"
@api_view(['GET'])
def get_top_games(request):
    try:
        number = int(request.GET.get('n'))
        results = GameList.objects.all()[:number]
        results_list = [obj.as_dict() for obj in results] # create a results_list to be converted to JSON format
        # # debugging ----
        # for result in results:
        #     obj = result.as_dict()
        #     print(obj['game_name'] + " / " + str(obj['num_player']))
        # # ---- end debugging
        outputJSON = json.dumps({"results": results_list}, ensure_ascii=False).encode('utf16')
        return HttpResponse(outputJSON, content_type='application/json')
    except:
        return HttpResponse('{"message":"input invalid", "get-top-games":{}}')


# Return average rating of a given a game_id #TODO or game name?
# TODO need to test,
# TODO might replace with storing average rating and number of ratings in table
@api_view(['GET'])
def get_average_rating(request):
    target_game_id = request.GET.get('gameid')
    games = Rating.filter(game_id__exact=target_game_id)
    if len(games) != 0:
        ratings_list = [obj.as_dict() for obj in games]
        average = str(sum(d['rate'] for d in ratings_list)/len*ratings_list) # convert to string for json

        return HttpResponse('''
                    {
                        "average-rating":%s
                    }    
                '''.format(average))
    else:
        return HttpResponse('{"message":"input invalid", "average-rating":{}}')


# Save a rating or review
# TODO need to test
# For testing
# curl -d '{"rating": {"username":"IHMS","gameid":4, "rate":4, "comment":"mada mada"} }' -X POST "http://localhost:8000/backend/rating/"
# curl http://localhost:8000/backend/login/ -X POST -d '{"user":{"username":"IHMS","password":"123456"}}'
@api_view(['POST'])
def rating(request):
    json_obj = None
    try:
        json_obj = json.loads(request.body.decode())
    except:
        print("Error when loading the Json")
        return HttpResponse('{"message":"input invalid", "rating":{}}')

    try:
        # Checks if player exist in database
        # Checks if game exist in database
        # Unsuccessful if either check throws does not exist
        user_id = User.objects.get(user_name=json_obj['rating']['username'])
        game_id = GameList.objects.get(game_id=json_obj['rating']['gameid'])
        rate = int(json_obj['rating']['rate']) # Asserts that rating is an integer
        comment = json_obj['rating']['comment']

        new_entry = Rating(user_id=user_id, game_id=game_id, rate=rate, comment=comment)
        new_entry.save()
        return HttpResponse('''
            {
                "message":"Successful"
            }    
        ''')
    except:
        return HttpResponse('''
            {
                "message":"Invalid Request"
            }
        ''')

# Gives 5 game recommendations for the given user
# For testing:
# TODO refactor below testing html for later
# curl -X GET "http://localhost:8000/backend/recommend_v1/?userid=76561197960530222"
@api_view(['GET'])
def recommend_v1(request):

    player = User.objects.get(user_id=request.GET.get('userid')) # Get the target user
    game_set = None
    try:
        game_set = PlayerLibrary.objects.filter(user_id=player)
    except:
        # If no games, for now, return top 5 current games
        # TODO discuss with group if they want this
        results = GameList.objects.all()[:5]
        results_list = [obj.as_dict() for obj in results]  # create a results_list to be converted to JSON format
        outputJSON = json.dumps({"results": results_list}, ensure_ascii=False).encode('utf-16')
        return HttpResponse(outputJSON, content_type='application/json')

    # Step 1: Get all player games
    player_games = []
    for entries in game_set:
        try: # To handle the weird db issue atm where we ignore if game is not there
            game_obj = entries.game_id
            game_id = game_obj.game_id
            player_games.append(game_id)
        except:
            continue

    # Step 2: Get all related genres
    genre_count = {}
    genre_set = Genres.objects.filter(game_id__in=player_games)
    for game_genre in genre_set:
        genre = game_genre.genre
        if genre in genre_count:
            genre_count[genre] += 1
        else:
            genre_count[genre] = 1

    # Step 3: Sort and get the top 5 genres
    top_5_genres = []
    sorted_keys = [(k, genre_count[k]) for k in sorted(genre_count, key=genre_count.get, reverse=True)] # [:2] # Just for debugging
    # debugging
    # for genre, count in sorted_keys:
    #     print(genre + "/" + str(count))

    for i in range(0,5):
        genre, count = sorted_keys[i % len(sorted_keys)]
        print(genre)
        top_5_genres.append(genre)

    # Filter all games list by genre, exclude duplicates when adding to recommend list
    print("Recommendations")
    recommend_set = []
    for genre in top_5_genres:
        target_games = Genres.objects.filter(genre=genre)
        results = GameList.objects.filter(game_id__in=target_games.values('game_id')).exclude(game_id__in=recommend_set)
        result_top_dict = results[0].as_dict()
        recommend_set.append(result_top_dict['game_id'])

    # Output results
    results = GameList.objects.filter(game_id__in=recommend_set)
    results_list = [obj.as_dict() for obj in results]  # create a results_list to be converted to JSON format
    outputJSON = json.dumps({"results": results_list}, ensure_ascii=False).encode('utf-16')
    return HttpResponse(outputJSON, content_type='application/json')

# given json contain username, email, and password
@api_view(['POST'])
def edit_profile(request):
    print("user edit function is running ...")
    print("")
    obj = None
    try:
        obj = json.loads(request.body.decode())
        print("decode success")
    except:
        print("Error when loading the Json")
        pass

    if obj is not None:
        # get user data
        username = obj['edit']['username']
        e = obj['edit']['email']
        p= obj['edit']['password']

        print("get the username:" +username)
        print("get the email:" + e)
        print("get the password:" + p)
        try:
            user = User.objects.get(user_name=obj['edit']['username'])
            try:
                email = obj['edit']['email']
                user.email = email
                user.save()
                try:
                    password = obj['edit']['password']
                    user.pass_word = password
                    user.save()
                    return HttpResponse('{"message": "change password and email"}')
                except:
                    return HttpResponse('{"message": "change email"}')
            #pass new value of email and password
            except:
                try:
                    password = obj['edit']['password']
                    user.pass_word = password
                    user.save()
                    return HttpResponse('{"message": "change password"}')
                except:
                    return HttpResponse('{"message": "no change occurs"}')
            return HttpResponse('{"message": "no change occurs"}')
        except:
            return HttpResponse('{"message": "no user"}')
