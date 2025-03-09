from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()

    class Meta:
        db_table = "all_users"

from django.db import models

class Golfer(models.Model):
    name = models.CharField(max_length=100)
    day_1_score = models.IntegerField()
    day_2_score = models.IntegerField()
    day_3_score = models.IntegerField()
    day_4_score = models.IntegerField()
    average_scores_dayoverday = models.DecimalField(max_digits=5, decimal_places=2)
    tier = models.IntegerField()

    class Meta:
        db_table = "all_golfers"
