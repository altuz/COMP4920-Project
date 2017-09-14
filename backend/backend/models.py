from django.db import models


# by default, field is not null
class User(models.Model):
    user_name = models.CharField(max_length=15, primary_key=True, db_index=True)
    email = models.TextField()
    pass_word = models.TextField()
    user_id = models.IntegerField()
    privacy = models.BooleanField()

class PlayerLibrary(models.Model):
    user_name = models.ForeignKey('User', on_delete=models.CASCADE, db_index=True)
    game_id = models.ForeignKey('GameList', on_delete=models.CASCADE, db_index=True)
    wish_list = models.BooleanField()
    played = models.BooleanField()

    # meta data is anything that's not a field such as ordering option
    class Meta:  # may need to use indexes
        # user_name and game_id together has to be unique
        unique_together = ('user_name', 'game_id')


class GameList(models.Model):
    game_id = models.IntegerField(primary_key=True, db_index=True)
    game_name = models.CharField(max_length=20, db_index=True)
    num_player = models.IntegerField()

    class Meta:
        # order the table by number of player descending order, faster for search
        order_with_respect_to = 'num_player'


class Categories(models.Model):
    game_id = models.ForeignKey('GameList', on_delete=models.CASCADE, db_index=True)
    category = models.CharField(max_length=20, db_index=True)


class Rating(models.Model):
    user_name = models.ForeignKey('User', on_delete=models.CASCADE, db_index=True)
    game_id = models.ForeignKey('GameList', on_delete=models.CASCADE, db_index=True)
    rate = models.IntegerField()
    comment = models.TextField(null=True)  # comment can be null


class Follow(models.Model):
    user_name = models.ForeignKey('User', on_delete=models.CASCADE, db_index=True)
    following = models.ForeignKey('User', on_delete=models.CASCADE, db_index=True)