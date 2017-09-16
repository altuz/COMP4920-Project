from django.test import TestCase
from django.test import Client
import json
# Create your tests here.


class SignUpTester(TestCase):

    def test_sign_up_check(self):
        print("")
        print("Running sign up test")
        # create a client request
        c = Client()
        json_str = json.dumps({'user_name': 'fred', 'email': 's1ase@gmail.com', 'pass_word': 'haha', 'privacy': False})
        c.post('/backend/sign_up/', data=json_str, content_type='application/json',
               HTTP_X_REQUESTED_WITH='XMLHttpRequest')

