import config

def user_create(username, password, email):
	# TODO Check with ryan to check if pw and confirm pw are checked in frontend

def user_login(username, password):
	# Step 1: Check if details are correct
	# query db
	# if not correct, return error

	# Step 2: Create a session 

	# Connect to database
	# print "Using psycopg2…"
	import psycopg2
	myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
	# doQuery( myConnection )
	myConnection.close()

	# # print "Using PyGreSQL…"
	# import pgdb
	# myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
	# # doQuery( myConnection )
	# cur = myConnection.cursor()

	# cur.execute( "SELECT")

	# myConnection.close()

def user_logout(username, session_id):
	# Flush specified users session
