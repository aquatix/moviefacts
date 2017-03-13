from __future__ import unicode_literals

from django.db import models

class Movie(models.Model):
    """ Title, year, plot """

    title = models.CharField(max_length=255)
    year = models.IntegerField(blank=True, null=True)
    plot = models.TextField(blank=True, null=True)
    runtime = models.IntegerField(blank=True, null=True)


class Actor(models.Model):
    """ Actor's names and movies """

    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=255, blank=True, null=True)
