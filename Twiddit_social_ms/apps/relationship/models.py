from django.db import models

class Relationship(models.Model):

    id = models.AutoField(primary_key = True)
    followerId = models.IntegerField(blank = False, null = False)
    followedId = models.IntegerField(blank = False, null = False)
    blocked = models.BooleanField(blank = False, null = False, default = False)
    createdDate = models.DateField(auto_now=False, auto_now_add=True)