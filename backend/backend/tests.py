from django.test import TestCase
from django.test import Client
import json
# Create your tests here.


def sign_up_check():
    # create a client request
    c = Client()
    json_str = json.dumps({'user_name': 'fred', 'email': 's1ase@gmail.com', 'pass_word': 'haha', 'privacy': False})
    c.post('/backend/sign_up/', data=json_str, content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')


sign_up_check()
