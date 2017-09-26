"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
import backend.views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^backend/login/', backend.views.user_login),
    url(r'^backend/register/', backend.views.user_register),
    url(r'backend/test_session', backend.views.test_session),
    url(r'^backend/edit_list/', backend.views.update_userlist),
    url(r'^backend/activate/(/w+)', backend.views.activate_user),
    url(r'^backend/search_game/', backend.views.search_game)
]
