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
python3 manage.py migrates
```

make superuser
```sh
python3 manage.py createsuperuser
Username:
Email:
Password
Password (again)
```

### NOTE TO SELF
If it goes well and we choose to publically release or make this repo public DON'T put config.py (database details) onto git
