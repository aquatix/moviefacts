from django.core.management.base import BaseCommand, CommandError
from movieapi.models import Movie, Actor
import base64
import codecs
import os
import re

class Command(BaseCommand):
    help = 'Import themoviedb.org by paging through the API'

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str)

    def save_movie(movie_item):
        # try to get existing item

        # update the model
        pass

    def handle(self, *args, **options):
        vote_average = 6.0
        runtime_gte = 65
        url = 'https://api.themoviedb.org/3/discover/movie?api_key={}&include_adult=false&vote_average.gte={}&with_runtime.gte={}&page=1'.format(settings.api_key, vote_average, runtime_gte)

        self.stdout.write('Done saving to database, action!')
