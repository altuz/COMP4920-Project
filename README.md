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
1. get_list_AppID.py: get json response from steam for all appid and store them locally at steam_data folder
2. check_name_content_match.py: remove the local stored steam files that name of the file doesn't match the content steam_id
3. insert_steam_data.py: from the locally stored steam game information insert them into data base
4. get_steamspy_data.py: assume steam_data already there, get all data from for all appid soted locally from steam spy and store them at steam_spy_data folder
5. insert_spy_data.py: update database base on all locally downloaded steam spy data
```

DB file:
```sh
DB Link: https://drive.google.com/open?id=0B1v0wP8Fb4XHVjlPdm9mVGlJQm8
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
https://docs.google.com/document/d/1ybrlhSn1DO2cbp_bfC83s_AkoA4p-WfEvxZPTM217Bg/edit
```

### NOTE TO SELF
If it goes well and we choose to publically release or make this repo public DON'T put config.py (database details) onto git
