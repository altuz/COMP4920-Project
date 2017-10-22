from backend.models import User, UserSerializer, Register, GameList, PlayerLibrary, Session, Follow, Categories, Rating, Genres
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from hashlib import blake2b
from django.db.models import Q
from functools import reduce
from django.db import connection
from django.db.models import Count
import django
import smtplib
import json
import time
import operator
from backend.graph import Graph

# Pass in user1 and user2

@api_view(['GET'])
def is_following(request):
    user1 = request.GET['user1']
    user2 = request.GET['user2']
    try:
        u1 = User.objects.get(user_name = user1)
        u2 = User.objects.get(user_name = user2)
        try:
            f = Follow.objects.get(user_id = u1, follow_id = u2)
            return HttpResponse('{ "message" : "user1 follows user2", "success" : "True" }')
        except:
            return HttpResponse('{ "message" : "user1 does not follow user2", "success" : "False" }')
    except:
        return HttpResponse('{ "message" : "either one or both users does not exist", "success" : "False" }')

def user_prof_helper(username):
    game_list = ""
    wish_list = ""
    user_prof = ""
    flw_list = ""
    # Get user
    try:
        user_entry = User.objects.get(user_name=username)
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
        game_list = get_list(username, True)
    except Exception as e:
        print(e)
        print("No games")
    # Get wish list
    try:
        wish_list = get_list(username, False)
    except:
        print("No wishes")
    # Get follow list
    try:
        flw_list = follow_list_helper(username)
    except:
        print("No follows")
    ret_json = '''
            {{
                "user" : "{}",
                "gamelist" : [{}],
                "wishlist" : [{}],
                "follows" : [{}]
            }}
        '''.format(username, game_list, wish_list, flw_list)
    return HttpResponse(ret_json)


# Retrieves user profile along with game list and wish list
# TESTED
# curl -X GET "http://localhost:8000/backend/user_prof/?username=a%20regular"
@api_view(['GET'])
def user_prof(request):
    return user_prof_helper(request.GET['username'])


# Follow user
# User1 -> User2
# Tested
# curl -d '{"user":{"user1" : "a regular", "user2" : "Jarmustard"}}' -X POST "http://localhost:8000/backend/follow_user/"
@api_view(['POST'])
def follow_user(request):
    json_obj = None
    # decode json
    try:
        json_obj = json.loads(request.body.decode())
    except:
        print("Error loading json")
        return HttpResponse('{"message" : "input invalid", "success" : "False"}')
    # check if user1 and user2 exists
    try:
        user_1 = User.objects.get(user_name = json_obj['user']['user1'])
        user_2 = User.objects.get(user_name = json_obj['user']['user2'])
        new_entry = Follow(user_id = user_1, follow_id = user_2)
        new_entry.save()
        return HttpResponse('{"message" : "Followed", "success" : "True"}')
    except Exception as e:
        print(e)
        return HttpResponse('{"message" : "User1 or User2 does not exist", "success" : "False"}')

# Unfollow user
# User1 -> User2
@api_view(['POST'])
def unfollow_user(request):
    json_obj = None
    # decode json
    try:
        json_obj = json.loads(request.body.decode())
    except:
        print("Error loading json")
        return HttpResponse('{"message" : "input invalid", "success" : "False"}')

    # check if user1 and user2 exists
    try:
        user_1 = json_obj['user']['user1']
        user_2 = json_obj['user']['user2']
        u1 = User.objects.get(user_name=user_1)
        u2 = User.objects.get(user_name=user_2)
        try:
            f = Follow.objects.get(user_id=u1, follow_id=u2)
            f.delete()
            return HttpResponse('{ "message" : "unfollow successful", "success" : "True" }')
        except:
            return HttpResponse('{ "message" : "user1 does not follow user2", "success" : "False" }')
    except Exception as e:
        print(e)
        return HttpResponse('{"message" : "User1 or User2 does not exist", "success" : "False"}')

# Get user's follow list
# Tested
# curl -d '{"user":{"username" : "a regular"}}' -X POST "http://localhost:8000/backend/follow_list/"
@api_view(['GET'])
def follow_list(request):
    try:
        ret_json = '''
            {{
                "message" : "success",
                "username" : "{}",
                "follows" : [
                    {}
                ]
            }}
            '''.format(request.GET.get('username'), follow_list_helper(request.GET.get('username')))
        return HttpResponse(ret_json)
    except:
        return HttpResponse('{"message" : "User does not exist", "success" : "False"}')


def follow_list_helper(name):
    try:
        follower = User.objects.get(user_name = name)
        following_list = Follow.objects.filter(user_id = follower)
        json_list = []
        for person in following_list:
            followed = person.follow_id
            f_name = followed.user_name.replace('"', '\\"')
            f_numg = followed.num_games
            f_json = '{{"user_name" : "{}", "num_games" : "{}"}}'.format(f_name, f_numg)
            json_list.append(f_json)

        follow_json = ",".join(json_list)
        return follow_json
    except Exception as e:
        print(e)


# Get reviews for a game
# example: curl -d '{"user":{"gameid" : "639790"}}' -X POST "http://localhost:8000/backend/get_reviews/"
# Tested
@api_view(['GET'])
def get_reviews(request):
    try:
        game    = GameList.objects.get(game_id = request.GET.get('gameid'))
        reviews = Rating.objects.filter(game_id = game)
        # Put 'results' querySet into dict format to convert into JSON dict
        json_list = []
        for review in reviews:
            try:
                reviewer = review.user_id
                r_name = reviewer.user_name
                r_bool = review.rate
                r_comment = review.comment
                f_json = '{{"user_name" : "{}", "rating" : "{}", "comment" : "{}"}}'.format(r_name, r_bool, r_comment)
                json_list.append(f_json)
            except:
                continue
        # results_list = [obj.as_dict() for obj in reviews]
        reviews_json = ",".join(json_list)
        ret_json = '''
                {{
                    "message" : "success",
                    "gameid" : "{}",
                    "reviews_list" : [
                        {}
                    ]
                }}
                '''.format(request.GET.get('gameid'), reviews_json)
        return HttpResponse(ret_json)
    except Exception as e:
        print(e)
        return HttpResponse('{"message" : "game does not exist", "success" : "False"}')


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
        #print(gamelist)
        # convert to json list
        for entries in gamelist:
            try:
                game = entries.game_id
                g_id = game.game_id
                g_name = game.game_name
                g_picture = game.image_url
                g_played_hrs = entries.played_hrs
                # print("played hours for " + str(g_name) + " is: " + str(g_played_hrs))
                if(g_played_hrs == None):
                    g_played_hrs = 0
                    # print("Adjusted played hours for " + str(g_name) + " is: " + str(g_played_hrs))
                g_json = '{{"game_name":"{}", "game_id":"{}", "thumbnail":"{}", "played_hrs":"{}"}}'.format(g_name, g_id, g_picture, g_played_hrs)
                g_json = '{{"game_name":"{}", "game_id":"{}", "thumbnail":"{}", "played_hrs":"{}"}}'.format(g_name, g_id, g_picture, g_played_hrs)
                json_list.append(g_json)
            except Exception as e:
                print(e)
                continue
        print(','.join(json_list))
        return ','.join(json_list)
    except Exception as e:
        print(e)
        raise e


# Get a user's game list
# TESTED
# curl -d '{"user":{"username" : "a regular"}}' -X POST "http://localhost:8000/backend/game_list/"
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
    except Exception as e:
        print(e)
        return HttpResponse('{"message":"does not exist, "gamelist":[]"}')


# Get a user's wish list
# curl -d '{"user":{"username" : "a regular"}}' -X POST "http://localhost:8000/backend/wish_list/"
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
# curl -d '{"user":{"username" : "a regular", "gameid" : "", "played" : False, "wish" : True}}' -X POST "http://localhost:8000/backend/edit_list/"
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
        player  = User.objects.get(user_name = json_obj['user']['username'])
        game    = GameList.objects.get(game_id = json_obj['user']['gameid'])
        played = json_obj['user']['played']
        wishes = json_obj['user']['wish']

        try:
            old_entry = PlayerLibrary.objects.get(user_id = player, game_id = game)
            old_entry.wish_list = wishes
            old_entry.played = played
            old_entry.save()
            if played is False and wishes is False:
                try:
                    user_rating = Rating.objects.get(user_id = player, game_id = game)
                    rate_val = user_rating.rate
                    rating_count = game.rating_count
                    average_rating = game.average_rating
                    total_rating = rating_count * average_rating
                    if rate_val is True:
                        total_rating -= 1
                    rating_count -= 1
                    new_average = total_rating/rating_count
                    game.rating_count = rating_count
                    game.average_rating = new_average
                    game.save()
                    user_rating.delete()
                except:
                    pass
        except:
            new_entry = PlayerLibrary(user_id=player, game_id=game, wish_list=wishes, played=played)
            new_entry.save()

        return user_prof_helper(json_obj['user']['username'])
    except Exception as e:
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
    print(obj)

    if obj is not None:
        # check user existence
        try:
            exist_user = User.objects.get(user_name=obj['user']['user_name'])
        #print(exist_user)
            return HttpResponse(msg_to_json("user already exist"))
        except:
            # create new user for the register table and get info from the request
            user_name = obj['user']['user_name']
            password = obj['user']['pass_word']
            key = blake2b((user_name + password).encode('utf-8')).hexdigest()  # key send to the user
            link = "http://localhost:8090/#/activate/" + key

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

    exist_register = Register.objects.get(key=key)

    # create the new user
    new_user = User(user_name=exist_register.user_name, email=exist_register.email,
                    pass_word=exist_register.pass_word, privacy=exist_register.privacy, num_games=0)
    new_user.save()

    # delete entry in the register table
    exist_register.delete()

    try:
        return HttpResponse(msg_to_json("used activated"))
    except django.db.utils.IntegrityError as e:
        print(e)
        return HttpResponse(msg_to_json("request failed"))

# Search for users
# Returns all users if no user is given
# For testing
# curl -X GET "http://localhost:8000/backend/search_user/?q=a%20regular"
@api_view(['GET'])
def search_user(request):
    print("search user function is running ...")
    print("")
    try:
        query = request.GET.get('q')
        # Step 1: Filter by keyword
        if query:
            query_list = query.split(" ")
            results = User.objects.filter(
                reduce(operator.and_, (Q(user_name__icontains=q) for q in query_list))
            )  # Returns a QuerySet
        else:
            results = User.objects.all()  # Return all the results if no key words are given

        # Put 'results' querySet into dict format to convert into JSON dict
        results_list = [obj.as_dict() for obj in results]
        outputJSON = json.dumps({"results": results_list}, ensure_ascii=False).encode('utf16')
        return HttpResponse(outputJSON, content_type='application/json')
    except:
        return HttpResponse('{"message":"input invalid", "search-games":{}}')

# Search for games
# For testing - note: %20 is a space, %2C is a comma in URL character encoding
# curl -X GET "http://localhost:8000/backend/search_game/?q=for%20left&category=strategy%2CRTS"
# curl -X GET "http://localhost:8000/backend/search_game/?q=soldier&category=Multi%2DPlayer&genre="
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
    try:
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
        outputJSON = json.dumps({"results": results_list}, ensure_ascii=False).encode('utf16')
        return HttpResponse(outputJSON, content_type='application/json')
    except:
        return HttpResponse('{"message":"input invalid", "search-games":{}}')

# TESTED
# Get the top "n" number of games
# curl -X GET "http://localhost:8000/backend/get_top_games/?n=100"
@api_view(['GET'])
def get_top_games(request):
    # Temporary code segment to analyse data
    # ---------------------------------------
    # # game_id = 578080 # PLAYERUNKNOWN'S BATTLEGROUNDS (PUBG)
    # # game_id = 113200 # Binding of isaac
    # # game_id = 319630 # Life is strange
    # target_game_id = 268910
    # target_game = GameList.objects.filter(game_id=target_game_id)
    # player_set = PlayerLibrary.objects.filter(game_id=target_game).exclude(played_hrs=0)
    
    # entries = []
    # for player in player_set:
    #     player_obj = player.user_id
    #     entry_dict = {}
    #     entry_dict['username'] = player_obj.user_name
    #     entry_dict['hrs'] = player.played_hrs
    #     entries.append(entry_dict)
    # for entry in entries:
    #     print(entry)
    # outputJSON = json.dumps(entries, ensure_ascii=False).encode('utf16')
    # return HttpResponse(outputJSON, content_type='application/json')
    # ---------------------------------------

    try:
        number = int(request.GET.get('n'))
        results = GameList.objects.all()[:number]
        results_list = [obj.as_dict() for obj in results] # create a results_list to be converted to JSON format
        outputJSON = json.dumps({"results": results_list}, ensure_ascii=False).encode('utf16')
        return HttpResponse(outputJSON, content_type='application/json')
    except:
        return HttpResponse('{"message":"input invalid", "get-top-games":{}}')

# TESTED
# Returns the game corresponding to given input gameid
# @param    gameid of target game, if userid is provided, returns true/false for if in that users game/wishlist
# @return   game with all it's contents
# Testing
# curl -X GET "http://localhost:8000/backend/get_game_info/?gameid=578080&username=a%20regular"
@api_view(['GET'])
def get_game_info(request):
    print("get_game_info function is running\n...")
    # Step 1: get the target game info
    try: # Case game exists
        game_id = int(request.GET.get('gameid'))
        target_game = [GameList.objects.get(game_id=game_id).as_dict()]
    except: # Case no matching game
        return HttpResponse('{"message":"invalid gameid", "get_game_info":{}')

    # Step 2: Get the games genre/categories
    game_obj = GameList.objects.get(game_id=game_id)
    genres_obj = Genres.objects.filter(game_id=game_obj)
    category_obj = Categories.objects.filter(game_id=game_obj)
    genre_list = []
    category_list = []
    for g in genres_obj:
        genre_list.append(g.genre)
    for c in category_obj:
        category_list.append(c.category)

    # Step 3: Collect the game reviews
    reviews = Rating.objects.filter(game_id=game_obj)
    # Put 'results' querySet into dict format to convert into JSON dict
    reviews_list = []
    for review in reviews:
        try:
            reviewer = review.user_id
            entry_dict = {}
            entry_dict['user_name'] = reviewer.user_name
            entry_dict['rating'] = review.rate
            entry_dict['comment'] = review.comment
            reviews_list.append(entry_dict)
        except:
            continue

    # Step 4: check if user paramter given, if given user logged in
    player_obj = None
    try: # if given loggen in user, check if on their game list
        player_obj = User.objects.get(user_name=request.GET.get('username'))
    except:
        # if no user
        print("output type1: No user logged in")
        outputJSON = json.dumps({"game_info": target_game,
                                 "genre_list": genre_list,
                                 "category_list": category_list,
                                 "in_game_list": "",
                                 "in_wish_list": "",
                                 "reviews_list": reviews_list,
                                 "user_review": ""},
                                ensure_ascii=False).encode('utf16')

    # Step 5: Display whether in player game/wish list
    if player_obj:
        game_set = PlayerLibrary.objects.filter(user_id=player_obj, game_id=game_obj)
        # print(game_set)
        if game_set:
            print("output type2: Game is in player library")
            wish_list = game_set[0].wish_list # Should only have one entry, get entry 0
            played = game_set[0].played # Should only have one entry, get entry 0

            # Step 6: Get their review if exists, should only have one entry
            review = Rating.objects.filter(user_id=player_obj, game_id=game_obj)
            user_review = {}
            if review:
                user_review['user_name'] = player_obj.user_name
                user_review['rating'] = review[0].rate
                user_review['comment'] = review[0].comment
                print(user_review)
                user_review_output = [user_review]
            else:
                user_review_output = []

            outputJSON = json.dumps({"game_info": target_game,
                                     "genre_list": genre_list,
                                     "category_list": category_list,
                                     "in_game_list": played,
                                     "in_wish_list": wish_list,
                                     "reviews_list": reviews_list,
                                     "user_review": user_review_output},
                                    ensure_ascii=False).encode('utf16')
        else:
            print("output type3: Game is NOT in player library")
            outputJSON = json.dumps({"game_info": target_game,
                                     "genre_list": genre_list,
                                     "category_list": category_list,
                                     "in_game_list": False,
                                     "in_wish_list": False,
                                     "reviews_list": reviews_list,
                                     "user_review": ""},
                                    ensure_ascii=False).encode('utf16')

    return HttpResponse(outputJSON, content_type='application/json')

# TESTED
# Save a rating or review
# curl -d '{"review": {"username":"a regular","gameid":"578080", "rate":"True", "comment":"mada mada"}}' -X POST "http://localhost:8000/backend/send_review/"
@api_view(['POST'])
def send_review(request):
    print("Send review")
    print("...")
    try:
        json_obj = json.loads(request.body.decode())
    except:
        print("Error when loading the Json")
        return HttpResponse('{"message":"input invalid", "rating":{}}')

    # Debugging
    # player = User.objects.get(user_name=json_obj['review']['username'])
    # game = GameList.objects.get(game_id=int(json_obj['review']['gameid']))
    # entry_set = Rating.objects.filter(user_id=player, game_id=game)
    # for entry in entry_set:
    #     print(entry)

    # Checks if player exist in database
    # Checks if game exist in database
    # Unsuccessful if either check throws does not exist
    try:
        player = User.objects.get(user_name=json_obj['review']['username'])
        game = GameList.objects.get(game_id=int(json_obj['review']['gameid']))
        rate_val = (str(json_obj['review']['rate']) == "True") # Asserts that rating is an integer
        comment = json_obj['review']['comment']
    except:
        return HttpResponse('''
            {
                "message":"Invalid Request"
            }
        ''')

    # Check if player has already reviewed this game
    try:
        # Update total game rating
        old_entry = Rating.objects.get(user_id=player, game_id=game) # Users old rating

        try:
            rating_count = game.rating_count
            average_rating = game.average_rating
            total_rating = rating_count * average_rating
            # print("rate_val " + str(rate_val) + " old_entry.rate " + str(old_entry.rate))
            if (rate_val is True) and (old_entry.rate is False):  # Increase if old was false
                total_rating += 1
                print("Total increased")
            elif (rate_val is False) and (old_entry.rate is True):
                total_rating -= 1
                print("Total decreased")
            new_average = total_rating / rating_count
            game.rating_count = rating_count
            game.average_rating = new_average
            game.save()
        except:
            pass

        # Update old rating
        old_entry.rate = rate_val
        old_entry.comment = comment
        old_entry.save()

        print("Updated old review")

    except:
        # Update total game rating
        try:
            rating_count = game.rating_count
            average_rating = game.average_rating
            total_rating = rating_count * average_rating
            if rate_val is True:
                total_rating += 1
                print("Total increased")
            rating_count += 1  # Increase rating count
            new_average = total_rating / rating_count
            game.rating_count = rating_count
            game.average_rating = new_average
            game.save()
        except:
            pass

        # Create new rating
        new_entry = Rating(user_id=player, game_id=game, rate=rate_val, comment=comment)
        new_entry.save()

        print("Made new review")

    return HttpResponse('''
        {
            "message":"Successful"
        }    
    ''')


# Gives 5 game recommendations for the given user
# curl -X GET "http://localhost:8000/backend/recommend_v1/?username=a%20regular"
# TESTED
@api_view(['GET'])
def recommend_v1(request):
    # Return error if user can't be found
    try:
        player = User.objects.get(user_name=request.GET.get('username')) # Get the target user
    except:
        return HttpResponse('{"message":"invalid user", "recommend":{}}')

    # game_set = None # Don't really need this since exception below would return
    try:
        game_set = PlayerLibrary.objects.filter(user_id=player)
        # # debugging
        # for game in game_set:
        #     print(game)
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
        top_5_genres.append(genre)

    # Step 4: Get top genres for output
    top_genres = []
    num = 0
    for genre, count in sorted_keys:
        if num < 5:
            top_genres.append(genre)
            num += 1
        else:
            break
        # print(str(genre) + " count: " + str(count))

    # Step 5: Filter all games list by similar genre of user, exclude duplicates when adding to recommend list
    print("5 Recommendations")
    recommend_set = []
    for genre in top_5_genres:
        target_games = Genres.objects.filter(genre=genre)
        results = GameList.objects.filter(game_id__in=target_games.values('game_id')).exclude(game_id__in=recommend_set).exclude(game_id__in=player_games)
        result_top_dict = results[0].as_dict()
        recommend_set.append(result_top_dict['game_id'])

    # Step 6: Output results
    results = GameList.objects.filter(game_id__in=recommend_set)
    # # debugging
    # for result in results:
    #     print(result)
    results_list = [obj.as_dict() for obj in results]  # create a results_list to be converted to JSON format
    # Add genre information for each game in result
    for result in results_list:
        game_obj = GameList.objects.get(game_id=result['game_id'])
        genres_obj = Genres.objects.filter(game_id=game_obj)
        genre_list = []
        for g in genres_obj:
            genre_list.append(g.genre)

        # Add genre and category information to output
        result['genre_list'] = genre_list
        # print(result)

    # Step 2: Get the games genre/categories
    game_obj = GameList.objects.get(game_id=game_id)
    genres_obj = Genres.objects.filter(game_id=game_obj)
    category_obj = Categories.objects.filter(game_id=game_obj)
    genre_list = []
    category_list = []
    for g in genres_obj:
        genre_list.append(g.genre)
    for c in category_obj:
        category_list.append(c.category)
    outputJSON = json.dumps({"results": results_list,
                             "top_genres": sorted_keys,
                             }, ensure_ascii=False).encode('utf-16')
    return HttpResponse(outputJSON, content_type='application/json')

# given json contain username, email, and password
# curl -d '{"edit":{"username" : "a regular", "email" : "edittest@gmail.com", "password" : "editpass"}}' -X POST "http://localhost:8000/backend/edit_profile/"
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
        p = obj['edit']['password']
        print("e" + e)
        print("p" + p)

        user_entry = User.objects.get(user_name=username)

        if e is '':
            e = user_entry.email

        if p is '':
            p = user_entry.pass_word

        user_entry.email = e
        user_entry.pass_word = p
        print("new email" + user_entry.email)
        print("new pass" + user_entry.pass_word)
        try:
            user_entry.save()
            return HttpResponse('{"message" : "edit success"}')
        except Exception as e:
            print(e)

    return HttpResponse('{"message": "no user"}')

# TESTED
# given json contain username, gameid, and hours
# curl -d '{"edit_game_hrs":{"username" : "a regular", "gameid" : "578080", "played_hrs" : "580"}}' -X POST "http://localhost:8000/backend/edit_game_hrs/"
@api_view(['POST'])
def edit_game_hrs(request):
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
        username = obj['edit_game_hrs']['username']
        gameid = obj['edit_game_hrs']['gameid']
        played_hrs = obj['edit_game_hrs']['played_hrs']

        try:
            user_entry = User.objects.get(user_name=username)
            game_entry = GameList.objects.get(game_id=gameid)
            library_entry = PlayerLibrary.objects.get(user_id=user_entry, game_id=game_entry)
        except:
            return HttpResponse('{"message" : "edit failure"}')

        # print("Old played hrs is " + str(library_entry.played_hrs))
        library_entry.played_hrs = played_hrs

        try:
            library_entry.save()
            # print("New played hrs is " + str(library_entry.played_hrs))

            # Return the updated gamelist
            # Initialise values
            game_list = ""
            # Get game list
            try:
                game_list = get_list(obj['edit_game_hrs']['username'], True)
            except:
                print("No games")

            ret_json = '''
                    {{
                        "gamelist" : [{}]
                    }}
                '''.format(game_list)
            response = HttpResponse(ret_json)
            return response
            # return HttpResponse('{"message" : "edit success"}')
        except Exception as e:
            print(e)

    return HttpResponse('{"message": "no user"}')

# TESTED
# Get the gamelist for specified user
# curl -X GET "http://localhost:8000/backend/get_game_list/?username=a%20regular"
@api_view(['GET'])
def get_game_list(request):
    # Initialise values
    game_list = ""
    # Get game list
    try:
        game_list = get_list(request.GET.get('username'), True)
    except:
        print("No games")

    ret_json = '''
                        {{
                            "gamelist" : [{}]
                        }}
                    '''.format(game_list)
    response = HttpResponse(ret_json)
    return response

game_graph = None
user_set = None
game_set = None

# curl -X GET "http://localhost:8000/backend/recommend_test/"
@api_view(['GET'])
def recommend_test(request):
    global game_graph, user_set, game_set
    # =====================================================
    # ---------Example from text book ---------------------
    user_set = {}
    game_set = {}
    game_graph = Graph()

    user_set = { '0':'1','1':'2','2':'3','3':'4','4':'5','5':'6','6':'7','7':'8','8':'9','9':'10'}
    game_set = { '0':'A','1':'B','2':'C','3':'D','4':'E'} 

    # params: game, user, hrs, rating 
    game_graph.connect_u_g("A", "1", 5, 5)
    game_graph.connect_u_g("A", "3", 5, 5)
    game_graph.connect_u_g("A", "5", 4, 4)
    game_graph.connect_u_g("A", "7", 3, 3)
    game_graph.connect_u_g("A", "8", 5, 5)

    game_graph.connect_u_g("B", "1", 4, 4) 
    game_graph.connect_u_g("B", "2", 3, 3) 
    game_graph.connect_u_g("B", "3", 2, 2)
    game_graph.connect_u_g("B", "6", 3, 3) 
    game_graph.connect_u_g("B", "9", 2, 2) 

    game_graph.connect_u_g("C", "1", 4, 4)  
    game_graph.connect_u_g("C", "2", 5, 5)
    game_graph.connect_u_g("C", "4", 3, 3)
    game_graph.connect_u_g("C", "7", 3, 3)
    game_graph.connect_u_g("C", "8", 4, 4)
    game_graph.connect_u_g("C", "9", 5, 5)
    game_graph.connect_u_g("C", "10", 5, 5)

    game_graph.connect_u_g("D", "4", 1, 1)
    game_graph.connect_u_g("D", "5", 4, 4)
    game_graph.connect_u_g("D", "6", 3, 3)
    game_graph.connect_u_g("D", "7", 2, 2)
    game_graph.connect_u_g("D", "9", 4, 4)
    game_graph.connect_u_g("D", "10", 3, 3)

    game_graph.connect_u_g("E", "2", 4, 4)
    game_graph.connect_u_g("E", "3", 3, 3)
    game_graph.connect_u_g("E", "4", 2, 2)
    game_graph.connect_u_g("E", "5", 5, 5)
    game_graph.connect_u_g("E", "5", 5, 5)
    game_graph.connect_u_g("E", "8", 5, 5)
    game_graph.connect_u_g("E", "10", 4, 4)

    # ------------------------------------------------------------------
    game_graph.add_names(user_set, game_set)
    #game_graph.games_hours_stats()
    game_graph.calculate_bias()
    game_graph.baseline_predictor()
    game_graph.show_baseline()
    return HttpResponse("test") 



# curl -X GET "http://localhost:8000/backend/recommend_v2/?username=a%20regular"
@api_view(['GET'])
def recommend_v2(request):
    # TODO always include the user
    # targetUser = request.GET.get('username')
    global game_graph, user_set, game_set

    # Step 1: Fetch corresponding player info
    try:
        our_user = User.objects.get(user_name=request.GET.get('username')) # Get the target user
    except:
        return HttpResponse('{"message":"invalid user", "recommend":{}}')

    try:
        game_list = PlayerLibrary.objects.filter(user_id=our_user)
    except:
        # If no games, for now, return top 5 current games
        # TODO discuss with Nick if we should still do this for recommend_v2
        results = GameList.objects.all()[:5]
        results_list = [obj.as_dict() for obj in results]  # create a results_list to be converted to JSON format
        outputJSON = json.dumps({"results": results_list}, ensure_ascii=False).encode('utf-16')
        return HttpResponse(outputJSON, content_type='application/json')

    # Step 2: Get all player games
    player_games = []
    for entries in game_list:
        try:  # To handle the weird db issue atm where we ignore if game is not there
            game_obj = entries.game_id
            game_id = game_obj.game_id
            player_games.append(game_id)
        except:
            continue

    # Step 3: Get predictions, match with db game_info exclude duplicates when adding to recommend list
    # TODO @Nicholas, test this, David's computer does not have enough memory to test
    print("5 Recommendations")
    predictionList = game_graph.baseline_predictor(our_user.user_id, 199)
    # sorted_predictionList = sorted(predictionList, key = lambda tuple : tuple[1], reverse = True) # Sort the predictions based on rating/ranking, highest to lowest
    recommend_set = []
    print("PredictionsList")
    for p in reversed(predictionList):
        results = GameList.objects.get(game_id = p[0]) #.exclude(game_id__in=recommend_set).exclude(game_id__in=player_games)
        if results.game_id in player_games:
            continue
        print("game_id: " + str(results.game_id) + ", game_name: "+ str(results.game_name) + ", Ranking/Rating: " + str(p[1]))
        result_top_dict = results.as_dict()
        recommend_set.append(result_top_dict['game_id'])

    # Step 4: Output results (ONLY TAKE TOP 5 MATCHES)
    results = GameList.objects.filter(game_id__in=recommend_set[:5])
    # # debugging
    # for result in results:
    #     print(result)
    results_list = [obj.as_dict() for obj in results]  # create a results_list to be converted to JSON format
    outputJSON = json.dumps({"results": results_list}, ensure_ascii=False).encode('utf-16')
    return HttpResponse(outputJSON, content_type='application/json')


def graph_setup():
    global game_graph, user_set, game_set
    if game_graph is None:
        print("Initializing Graph")

        #QUERY
        #
        # query = ''' SELECT  g.game_id as "game_id", g.game_name as "game_name",
        #                     u.user_id as "user_id", u.user_name as "user_name",
        #                     p.played_hrs as "played_hrs", r.rate as "rate"
        #             FROM backend_playerlibrary p
        #             LEFT JOIN backend_gamelist g
        #             ON g.game_id = p.game_id_id
        #             LEFT JOIN backend_user u
        #             ON u.user_id = p.user_id_id
        #             LEFT JOIN backend_rating r
        #             ON r.user_id_id = p.user_id_id
        #             AND r.game_id_id = p.game_id_id
        #             WHERE p.played_hrs != 0
        #             OR p.played_hrs != null;'''

        query = (' SELECT  g.game_id as "game_id", g.game_name as "game_name", \n'
                 '                            u.user_id as "user_id", u.user_name as "user_name", \n'
                 '                            p.played_hrs as "played_hrs", r.rate as "rate"\n'
                 '                    FROM backend_playerlibrary p\n'
                 '                    INNER JOIN (\n'
                 '                        SELECT *\n'
                 '                        FROM backend_gamelist\n'
                 '                        WHERE num_player > 100\n'
                 '                        ORDER BY num_player DESC\n'
                 '                        LIMIT 300\n'
                 '                    ) g\n'
                 '                    ON g.game_id = p.game_id_id\n'
                 '                    INNER JOIN (\n'
                 '                        SELECT *\n'
                 '                        FROM (\n'
                 '                            SELECT *\n'
                 '                            FROM backend_user\n' 
                #'                            ORDER BY RANDOM()\n'
                # '                            LIMIT 200\n' # Comment this line out to remove limit 
                 '                        ) y\n'
                 '                    ) u\n'
                 '                    ON u.user_id = p.user_id_id\n'
                 '                    LEFT JOIN backend_rating r\n'
                 '                    ON r.user_id_id = p.user_id_id\n'
                 '                    AND r.game_id_id = p.game_id_id\n'
                 '                    WHERE p.played_hrs != 0\n'
                 '                    OR p.played_hrs != null\n'
                 '                    AND p.played != 0\n'
                 '                    AND p.wish_list != 0\n;'
                 '                    ')
        cursor = connection.cursor()
        rows = cursor.execute(query)


        user_set = {}
        game_set = {}
        game_graph = Graph()
        library_len = 0
        for entry in rows:
            game = entry[0]
            user = entry[2]
            # Get related rating
            rate_val = -1
            # If there is a rating
            rate_bool = entry[5]
            if rate_bool is not None:
                rate_val = 1 if rate_bool else 0
            # TODO: Enter rate_val to edge
            user_set[user] = entry[3]
            game_set[game] = entry[1]
            game_graph.connect_u_g(game, user, entry[4], rate_val)
            library_len += 1
        print("Graph initialized")
        game_graph.add_names(user_set, game_set)
        # game_graph.games_hours_stats()
        game_graph.calculate_bias()

        query2 = "SELECT user_id_id, follow_id_id FROM backend_follow;"
        rows = cursor.execute(query2)
        for row in rows:
            game_graph.connect_u_u(row[0], row[1])
        print("Inserted {} edges to Graph".format(library_len))
