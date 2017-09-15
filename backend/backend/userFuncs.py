import config
from backend.models import User

def user_create(username, password, email):
	# TODO Check with ryan to check if pw and confirm pw are checked in frontend
    return -1

def user_login(username, password):
    single_entry = User.get(user_name = username, pass_word = password)

def user_logout(username, session_id):
	# Flush specified users session
    return -1