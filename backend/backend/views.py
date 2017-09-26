from backend.models import User, UserSerializer, Register, GameList, PlayerLibrary, Session
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

#PlayerLibrary
#user_name
#game_id
#wish_list
#played
@api_view(['POST'])
def update_userlist(request):
    obj = None
    try:
        # Checks if player exist in database
        # Checks if game exist in database
        # Unsuccessful if either check throws does not exist
        player  = User.objects.get(user_name = request.POST.get('username'))
        game    = GameList.objects.get(game_id = request.POST.get('game_id'))
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
    return None
# curl -d "param1=value1&param2=value2" -X POST http://localhost:3000/data
@api_view(['POST'])
def user_login(request):
    obj = None
    single_entry = None
    #Check if user is activated
    try:
        obj = json.loads(request.body.decode())
        print(obj)
    except:
        print("Error when loading the Json")
        pass

    try:
        single_entry = Register.objects.get(user_name = obj['user']['username'])
        # If it doesn't throw exception, user has not activated
        return HttpResponse('{"message":"account not activated", "user":{}}')
    except:
        try:
            single_entry = User.objects.get(user_name=obj['user']['username'],
                                            pass_word=obj['user']['password'])
        except:
            return HttpResponse('{"message":"does not exist, "user":{}"}')

    # Session
    # user_id
    # session_id
    # Get time and hash.
    # Insert it as session
    user_session = blake2b(str(time.time()).encode('utf-8')).hexdigest()

    new_session = Session(user_id = single_entry, session_id = user_session)
    new_session.save()
    response = HttpResponse(objs_to_json(single_entry))
    response.set_cookie('session_id', user_session);
    return response

@api_view(['POST'])
def test_session(request):
    request.session.sessionkey = 'ivb2jmftgbv3z97nnyfqtpwlpn1qv97k'
    print(request.session.get('username', "Not here"))
    return HttpResponse('{"test":"' + request.session.get('username', "Hello") + '"}')

@api_view(['POST'])
def check_session(request):
    obj = None
    single_entry = None
    try:
        ses_hash = blake2b(request.POST.get('username') + request.POST.get('ip_address'))
    except:
        return None

def user_logout(username, session_id):
    # Flush specified users session
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