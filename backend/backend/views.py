from backend.models import User, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
import json


def user_create(username, password, email):
    # TODO Check with ryan to check if pw and confirm pw are checked in frontend
    return -1


# curl -d "param1=value1&param2=value2" -X POST http://localhost:3000/data
@api_view(['POST'])
def user_login(request):
    obj = None
    # try:
    #     obj = json.loads(request.body.decode('utf-8'))
    # except:
    #     pass
    # if obj is None:
    #     return HttpResponse('"{message":"no request"}')
    single_entry = None
    try:
        single_entry = User.objects.get(user_name=request.POST.get('username'), pass_word=request.POST.get('password'))
    except:
        return HttpResponse('{"message":"does not exist"}')

    return HttpResponse(objs_to_json(single_entry))


def user_logout(username, session_id):
    # Flush specified users session
    return -1


def objs_to_json(objs):
    serializer = UserSerializer(objs)
    decoded_str = JSONRenderer().render(serializer.data).decode()
    return msg_with_data(decoded_str)


def msg_with_data(json_obj):
    return '{"message":"success", "data":%s}' % json_obj


def msg_to_json(msg):
    return '{"message":"%s"}' % msg


# user sign_up
@api_view(['POST'])
def user_sign_up(request):
    """
    post method function, get user information and try to sign up for him
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
        # create new user for the table and get info from the request
        new_user = User(user_name=obj['user_name'], email=obj['email'], pass_word=obj['pass_word'], privacy=obj['privacy'])
        new_user.save()
        return HttpResponse(msg_to_json("account created successfully"))
    else:
        return HttpResponse(msg_to_json("json loading failed"))
