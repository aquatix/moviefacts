from __future__ import unicode_literals

from django.db import models

class Movie(models.Model):
    """ Title, year, plot """

    title = models.CharField(max_length=255)
    year = models.DateField(blank=True)
    plot = models.TextField(blank=True)
    runtime = models.IntegerField(blank=True)


class Actor(models.Model):
    """ Actor's names and movies """

    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=255, blank=True)
