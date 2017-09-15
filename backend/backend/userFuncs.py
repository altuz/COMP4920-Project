from models import User, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
import json

def user_create(username, password, email):
	# TODO Check with ryan to check if pw and confirm pw are checked in frontend
    return -1
#curl -d "param1=value1&param2=value2" -X POST http://localhost:3000/data
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
        single_entry = User.objects.get(user_name = request.POST.get('username'), pass_word = request.POST.get('password'))
    except:
        return HttpResponse('"{message":"does not exist"}')

    return HttpResponse(objs_to_json(single_entry))

def user_logout(username, session_id):
	# Flush specified users session
    return -1

def objs_to_json (objs):
    serializer = UserSerializer(objs)
    decodedStr = JSONRenderer().render(serializer.data).decode()
    return msg_with_data(decodedStr)

def msg_with_data (jsonObj):
    return '"{message":"success", "data":%s}' % (jsonObj)