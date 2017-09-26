from backend.models import User, UserSerializer, Register, GameList, PlayerLibrary, Session, Follow
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from django.shortcuts import  render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from hashlib import blake2b
import smtplib
from django.core.mail import send_mail
import json
import time

# TODO: retrieve user profile, to be shown in profile page
@api_view(['GET'])
def user_prof(request):
    game_list = ""
    wish_list = ""
    user_prof = ""
    # Get user
    try:
        user_entry = User.objects.get(user_name = request.GET['username'])
        user_prof = '''
            { 
                "username" : "%s",
                "user_id" : "%s"
            }
        '''.format(user_entry.user_name, user_entry.user_id)
    except:
        HttpResponse('{ "user" : {}, "gamelist" : {}, "wishlist" : {} }')
    # Get game list
    try:
        game_list = get_gamelist(request.GET['username'], True)
    except:
        print("No games")
    # Get wish list
    try:
        wish_list = get_gamelist(request.GET['username'], False)
    except:
        print("No wishes")

    ret_json = '''
        {
            "user" : %s,
            "gamelist" : [%s],
            "wishlist" : [%s]
        }
    '''.format(user_prof, game_list, wish_list)
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
def get_list(username, type):
    # retrieve database objects
    try:
        # check if player exist
        # find gamelist related to player
        player = User.objects.get(username)
        gamelist = None
        if type is True:
            gamelist = PlayerLibrary.objects.filter(user_name=player, played=True)
        else:
            gamelist = PlayerLibrary.objects.filter(user_name=player, played=False, wish_list=True)
        json_list = []
        # convert to json list
        for entries in gamelist:
            game = entries.game_id
            g_id = game.game_id
            g_name = game.game_name
            g_json = '{"game_name":"%s", "game_id":"%s"}'.format(g_name, g_id)
            json_list.append(g_json)
        return ','.join(json_list)
    except Exception as e:
        raise e
# Get a user's game list
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
            {
                "message":"success",
                "gamelist": [
                    %s
                ]
            }
        '''.format(','.join(game_list))
        return HttpResponse(ret_json)
    except:
        return HttpResponse('{"message":"does not exist, "gamelist":[]"}')

# Get a user's wish list
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
        game_list = get_list(json_obj['user']['username'], True)
        # construct json object
        ret_json = '''
            {
                "message":"success",
                "wishlist": [
                    %s
                ]
            }
        '''.format(','.join(game_list))
        return HttpResponse(ret_json)
    except:
        return HttpResponse('{"message":"does not exist, "wishlist":[]"}')
# Adding a game to a user's wish or played list
@api_view(['POST'])
def update_userlist(request):
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
        played  = request.POST.get('played', False)
        wishes  = request.POST.get('wish', True)
        new_entry = PlayerLibrary(user_name = player, game_id = game, wish_list = wishes, played = played)
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
def user_login(request):
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

    # Session
    # user_id
    # session_id
    # Get time and hash.
    # Insert it as session
    #user_session = blake2b(str(time.time()).encode('utf-8')).hexdigest()

    #new_session = Session(user_id = user_entry, session_id = user_session)
    #new_session.save()
    response = HttpResponse(objs_to_json(user_entry))
    # response.set_cookie('session_id', user_session);
    # response.set_cookie('username', obj['user']['username']
    return response

@api_view(['POST'])
def check_session(request):
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
        response = HttpResponse(objs_to_json(user_entry))
    except:
        return HttpResponse('{"message":"does not exist or session invalid", "user":{}}')


def user_logout(username, session_id):
    response = HttpResponse('{"message":"success"}')
    response.delete_cookie('session_id')
    response.delete_cookie('username')
    return -1


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
def user_register(request):
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
        exist_user = User(user_name=obj['user_name'])
        if exist_user is not None:
            return HttpResponse(msg_to_json("user already exist"))

        # create new user for the register table and get info from the request
        key = blake2b("%s,%s,%s" % (obj['user_name'], obj['email'], obj['pass_word']))  # key send to the user
        link = "http://domainName.com/activate/" + key

        # send activation email
        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login('yun553966858@gmail.com', 'asdqwienvlasdkf')
            message = 'Subject: {}\n\n{}'.format("SteamR Registration",
                                                 "User Name: %s\nActivation Link: %s\n" % (obj['user_name'], link))
            server.sendmail('SteamR Team', obj['email'], message)
            server.quit()
        except smtplib.SMTPException:
            return HttpResponse(msg_to_json("fail to send email"))

        new_register = Register(user_name=obj['user_name'], email=obj['email'],
                                pass_word=obj['pass_word'], privacy=obj['privacy'], key=key)
        new_register.save()
        return HttpResponse(msg_to_json("register created successfully"))
    else:
        return HttpResponse(msg_to_json("json loading failed"))


# activate user, put user into user table
@api_view(['GET'])
def activate_user(request, key):
    """
    function that try to sign up a registered user (activate a user)
    :param request:
    :param key: activation key
    :return: if activation key exist create the user account in the table and return true, else return json no exist
    """
    exist_register = Register(key=key)
    if exist_register is None:
        return HttpResponse(msg_to_json("no exist"))

    # create the new user
    new_user = User(user_name=exist_register.user_name, email=exist_register.email,
                    pass_word=exist_register.pass_word, privacy=exist_register.privacy)
    new_user.save()

    # delete entry in the register table
    exist_register.delete()
    
    return HttpResponse(msg_to_json("used activated"))

# Search for games
# FOr testing
# curl -X GET http://localhost:8000/backend/search_game/?q=no_space_query
@api_view(['GET'])
def search_game(request):
    """
    function that searches for games matching search criteria
    :param request: the search request
    :return: if search match, return match list, else return json does not exist
    """
    print("search game function is running ...")
    print("")
    query = request.GET.get('q')
    # TODO Later, do a combined search with category, only checking if query is empty for now
    # TODO how to test by feeding a url with spaces?
    if query:
        query_list = query.split() # TODO for more advanced search later
        results = GameList.objects.filter(game_name__icontains=query)
        print("the results are")
        print(results)
        # TODO turn this into a JSON object

    return HttpResponse(msg_to_json("search performed"))