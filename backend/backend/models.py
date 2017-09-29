from django.db import models
from rest_framework import serializers


# by default, field is not null
class User(models.Model):
    user_id = models.AutoField(primary_key=True, db_index=True)
    user_name = models.CharField(max_length=15, db_index=True)
    email = models.CharField(max_length=30)
    pass_word = models.CharField(max_length=30)
    privacy = models.BooleanField()

    def __str__(self):
        return self.user_name


# user_id, session
class Session(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, db_index=True)
    session = models.CharField(max_length=256, db_index=True)

    class Meta:
        unique_together = ('user_id', 'session_id')

    def __str__(self):
        return str(self.user_id) + '/' + str(self.session_id)


# PlayerLibrary, user_name, game_id, wish_list, played
class PlayerLibrary(models.Model):
    user_name = models.ForeignKey('User', on_delete=models.CASCADE, db_index=True)
    game_id = models.ForeignKey('GameList', on_delete=models.CASCADE, db_index=True)
    wish_list = models.BooleanField()
    played = models.BooleanField()

    # meta data is anything that's not a field such as ordering option
    class Meta:  # may need to use indexes
        # user_name and game_id together has to be unique
        unique_together = ('user_name', 'game_id')

    def __str__(self):
        return str(self.user_name) + '/' + str(self.game_id)


class GameList(models.Model):
    game_id = models.IntegerField(primary_key=True, db_index=True)
    game_name = models.TextField(db_index=True)
    num_player = models.IntegerField()
    image_url = models.TextField()
    game_description = models.TextField(db_index=True)
    average_rating = models.FloatField()
    rating_count = models.IntegerField()

    class Meta:
        # order the table by number of player descending order, faster for search
        order_with_respect_to = 'num_player'

    def __str__(self):
        return str(self.game_id) + "/" + str(self.game_name)

    # dict for use with game_search
    def as_dict(self):
        return {
            "game_id": self.game_id,
            "game_name": self.game_name,
            "num_player": self.num_player
        }


class Categories(models.Model):
    game_id = models.ForeignKey('GameList', on_delete=models.CASCADE, db_index=True)
    category = models.CharField(max_length=20, db_index=True)

    def __str__(self):
        return str(self.game_id) + "/" + str(self.category)


class Rating(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, db_index=True)
    game_id = models.ForeignKey('GameList', on_delete=models.CASCADE, db_index=True)
    rate = models.IntegerField()
    comment = models.TextField(null=True)  # comment can be null
    rated_time = models.DateTimeField(auto_now_add=True)  # add current time stamp

    def as_dict(self):
        return {
            "user_id": self.user_id,
            "game_id": self.game_id,
            "rate": self.rate,
            "comment": self.comment
        }


class Follow(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, db_index=True)
    follow_id = models.ForeignKey('User', on_delete=models.CASCADE, db_index=True)


class Register(models.Model):
    user_name = models.CharField(primary_key=True, max_length=15)
    email = models.CharField(max_length=30)
    pass_word = models.CharField(max_length=30)
    privacy = models.BooleanField()
    key = models.TextField(db_index=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
