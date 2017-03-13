from django.core.management.base import BaseCommand, CommandError
from movieapi.models import Movie, Actor
import os

class Command(BaseCommand):
    help = 'Import the imdb files from the specified directory'

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str)

    def parse_movie_line(self, line):
        # Movies:
        # Se7en (1995)                                            1995
        # Series (skip):
        # "Family Guy" (1999)                                     1999-????
        # "Family Guy" (1999) {8 Simple Rules for Buying My Teenage Daughter (#4.8)}      2005
        if line[0] == '"':
            # It's a serie entry, skip
            return None, None
        else:
            year = line[-4:]
            stripped = line[:-4].strip()
            pieces = line.split('(')
            title = pieces[0].strip()
            return title, year

    def import_movies(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            linecounter = 0
            while not 'MOVIES LIST' in lines[linecounter]:
                linecounter += 1
            linecounter += 2

            title, year = self.parse_movie_line(lines[linecounter])
            if title:
                movie = Movie(title=title, year=year)
                movie.save()

    def handle(self, *args, **options):
        self.stdout.write('Importing IMDb files from "%s"' % options['directory'])


        movies_file = os.path.join(options['directory'], 'movies.list')
        self.stdout.write('Processing ' + movies_file)
        if os.path.isfile(os.path.join(options['directory'], 'movies.list')):
            self.import_movies(movies_file)
        else:
            self.stderr.write(movies_file + ' not found')
            return 1
