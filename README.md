# COMP4920-Project
## instruction:
### frontend:
```sh
$ cd frontend
```
run the following command first if package.json was modified
```sh
$ npm install
```
otherwise run the following command straightaway:
```sh
$ npm run dev
```

### backend:
backend is the main app for our project.
python version:
```sh
python 3.6
```
Django version:
```sh
Django 1.11.5
```
pakage needed:
```sh
pip3 install django-cors-headers
pip install djangorestframework
```
open another terminal, and cd to project directory
```sh
$ cd backend 
$ python manage.py runserver
```

update database
```sh
rm all cache files, rm the db file
python3.6 manage.py migrate --fake backend zero
python3.6 manage.py migrates
```

make superuser
```sh
python3 manage.py createsuperuser
Username:
Email:
Password
Password (again)
```

Initialise DataBase, script running order
```sh
fill the db:
1. make sure all following folder exist in current directory:
    * steam_data
    * steam_spy_data
    * friend_list.txt
    * steam_game_review
    * friend_data
    * user_data
    * extend_review
    * mysqlite.db
2. python3 insert_steam_data.py
3. python3 insert_spy_data.py
4. python3 insert_users.py 
5. python3 insert_friend_list.py
6. python3 insert_rating_count_to_game_list.py
7. python3 insert_reviews_for_users.py


scrapping data:
1. python3 get_steam_game_data.py (get all steam game stats store at steam_data)
2. python3 get_steam_spy_data.py (get all steam spy game stats store at steam_spy_data, depends on steam_data)
3. python3 get_user_id.py (get number of user_id and store at friend_list.txt, use bfs to build a friend tree)
4. python3 get_user_data_from_friend_list.py (get user_info, user_games and store at user_data, depends on friend_list.txt)
5. python3 get_friend_list.py (get friend list of each user and store at friend_data, depends on friend_list.txt)
6. python3 get_game_review.py (get game reviews for all games)
7. python scraper.py (get games review which more than 20)
```

DB file:
```sh
DB Link: https://drive.google.com/file/d/0B088tAJfImVlUnh3c0N6dnNHRm8/view?usp=sharing
```

Scraper Link:
```sh
Link: https://drive.google.com/open?id=0B1v0wP8Fb4XHNTRsZEFydzRRN2c

Instruction:

Python 2.7+
    pip install requests beautifulsoup4 unicodecsv

lxml [Windows](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml), [other os](http://lxml.de/installation.html)
```

Sprint Retrospective Link (Google docs):
```sh
https://docs.google.com/document/d/1ybrlhSn1DO2cbp_bfC83s_AkoA4p-WfEvxZPTM217Bg/edit?usp=sharing
```

### NOTE TO SELF
If it goes well and we choose to publically release or make this repo public DON'T put config.py (database details) onto git
