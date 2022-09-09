from django.db import models


class Nomination(models.Model):
    year = models.IntegerField(default=0)
    title = models.CharField(max_length=200)
    studios = models.CharField(max_length=200)
    producers = models.CharField(max_length=200)
    winner = models.BooleanField(default=False)