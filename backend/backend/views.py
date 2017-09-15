from django.utils import timezone
import json

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer

from backend.models import *

# user sign_up
@api_view(['POST'])
def user_sign_up(request):
    obj = None
    try:
        obj = json.loads(request.body.decode())
    except:
        print("Error when loading the Json")
        pass

    if obj is not None:
        # creat new user for the table and get info from the request
        new_user = User(user_name=obj['user_name'], email=obj['email'], pass_word=obj['pass_word'], privacy=obj['privacy'])
        new_user.save()
        return HttpResponse( True )
    else:
        return HttpResponse( False )
