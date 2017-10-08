from django.db import models
from rest_framework import serializers


# by default, field is not null
class User(models.Model):
    user_id = models.AutoField(primary_key=True, db_index=True)
    user_name = models.CharField(max_length=15, db_index=True)
    email = models.CharField(max_length=30, db_index=True)
    pass_word = models.CharField(max_length=30, db_index=True)
    privacy = models.BooleanField(db_index=True)
    num_games = models.IntegerField(db_index=True)

    def __str__(self):
        return str(self.user_id) + "/" + str(self.user_name)

    def as_dict(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "email": self.email,
            "privacy" : self.privacy,
            "num_games": self.num_games
        }

# user_id, session
class Session(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, db_index=True)
    session_id = models.CharField(max_length=256, db_index=True)

    class Meta:
        unique_together = ('user_id', 'session_id')

    def __str__(self):
        return str(self.user_id) + '/' + str(self.session_id)


# PlayerLibrary, user_name, game_id, wish_list, played
class PlayerLibrary(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, db_index=True)
    game_id = models.ForeignKey('GameList', on_delete=models.CASCADE, db_index=True)
    wish_list = models.BooleanField(db_index=True)
    played = models.BooleanField(db_index=True)
    played_hrs = models.IntegerField(null=True, db_index=True)

    # meta data is anything that's not a field such as ordering option
    class Meta:  # may need to use indexes
        # user_name and game_id together has to be unique
        unique_together = ('user_id', 'game_id')

    def __str__(self):
        return str(self.user_id) + '/' + str(self.game_id) + '\n'

    def as_dict(self):
        return {
            "user_id": self.user_id,
            "game_id": self.game_id,
            "wish_list": self.wish_list,
            "played": self.played,
            "played_hrs": self.played_hrs
        }


class GameList(models.Model):
    game_id = models.IntegerField(primary_key=True, db_index=True)
    game_name = models.TextField(db_index=True)
    num_player = models.IntegerField(null=True, db_index=True)
    image_url = models.TextField(db_index=True)
    game_description = models.TextField(db_index=True)
    support_language = models.TextField(null=True, db_index=True)
    required_age = models.IntegerField(db_index=True)
    developer = models.TextField(null=True, db_index=True)
    publisher = models.TextField(null=True, db_index=True)
    linux = models.BooleanField(db_index=True)
    mac = models.BooleanField(db_index=True)
    windows = models.BooleanField(db_index=True)
    price = models.FloatField(null=True, db_index=True)
    average_rating = models.FloatField(null=True, db_index=True)
    rating_count = models.IntegerField(null=True, db_index=True)

    class Meta:
        # order the table by number of player descending order, faster for search
        ordering = ['-num_player']

    # dict for use with game_search
    def as_dict(self):
        return {
            "game_id": self.game_id,
            "game_name": self.game_name,
            "num_player": self.num_player,
            "image_url": self.image_url,
            "game_description": self.game_description,
            "support_language": self.support_language,
            "required_age": self.required_age,
            "developer": self.developer,
            "publisher": self.publisher,
            "linux": self.linux,
            "mac": self.mac,
            "windows": self.windows,
            "price": self.price,
            "average_rating": self.average_rating,
            "rating_count": self.rating_count
        }

    def __str__(self):
        return str(self.game_id) + "/" + str(self.game_name) + "/" + str(self.num_player)


class Categories(models.Model):
    game_id = models.ForeignKey('GameList', on_delete=models.CASCADE, db_index=True)
    category = models.TextField(db_index=True)

    def as_dict(self):
        return {
            "game_id": self.game_id,
            "category": self.category
        }

    def __str__(self):
        return str(self.game_id) + "/" + str(self.category)


class Genres(models.Model):
    game_id = models.ForeignKey('GameList', on_delete=models.CASCADE, db_index=True)
    genre = models.TextField(db_index=True)

    def as_dict(self):
        return {
            "game_id": self.game_id,
            "genre": self.genre
        }

    def __str__(self):
        return str(self.game_id) + "/" + str(self.genre)


class Rating(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, db_index=True)
    game_id = models.ForeignKey('GameList', on_delete=models.CASCADE, db_index=True)
    rate = models.BooleanField(db_index=True)
    comment = models.TextField(null=True, db_index=True)  # comment can be null
    rated_time = models.DateTimeField(auto_now_add=True, db_index=True)  # add current time stamp

    def as_dict(self):
        return {
            "user_id": self.user_id,
            "game_id": self.game_id,
            "rate": self.rate,
            "comment": self.comment,
            "rated_time": self.rated_time
        }


class Follow(models.Model):
    user_id = models.ForeignKey('User', related_name= "follower_id", on_delete=models.CASCADE, db_index=True)
    follow_id = models.ForeignKey('User', related_name= "followed_id", on_delete=models.CASCADE, db_index=True)

    def as_dict(self):
        return {
            "user_id": self.user_id,
            "follow_id": self.follow_id
        }

    def __str__(self):
        return str(self.user_id) + "/follows-->/" + str(self.follow_id)

class Register(models.Model):
    user_name = models.CharField(primary_key=True, max_length=15, db_index=True)
    email = models.CharField(max_length=30, db_index=True)
    pass_word = models.CharField(max_length=30, db_index=True)
    privacy = models.BooleanField(db_index=True)
    key = models.TextField(db_index=True)

    def __str__(self):
        return str(self.user_name) + "/" + str(self.email) + "/" + str(self.pass_word) + "/" + str(self.privacy) + "/" + str(self.key)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
