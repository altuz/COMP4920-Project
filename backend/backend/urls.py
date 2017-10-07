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
import backend.views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^backend/login/', backend.views.login),
    url(r'^backend/register/', backend.views.register),
    url(r'^backend/edit_list/', backend.views.edit_list),
    url(r'^backend/search_game/', backend.views.search_game),
    url(r'^backend/game_list/', backend.views.get_gamelist),
    url(r'^backend/wish_list/', backend.views.get_wishlist),
    url(r'^backend/follow_user/', backend.views.follow_user),
    url(r'^backend/session_check/', backend.views.session_check),
    url(r'^backend/logout/', backend.views.logout),
    url(r'^backend/user_prof/', backend.views.user_prof),
    #url(r'^backend/activate/(/w+)', backend.views.activate_user),
    url(r'^backend/rating/', backend.views.rating),
    url(r'^backend/recommend_v1/', backend.views.recommend_v1),
    url(r'^backend/get_top_games/', backend.views.get_top_games),
    url(r'^backend/check_in_userlist/', backend.views.check_in_userlist)
]
