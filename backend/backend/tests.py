from django.test import TestCase
from django.test import Client
# Create your tests here.

def sign_up_check():
    # create a client request
    c = Client()
    c.post('/backend/sign_up', {'user_name': 'fred', 'email': 's1ase@gmail.com', 'pass_word': 'haha', 'privacy': False})

if __name__ == "__main__":
