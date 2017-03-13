from django.core.management.base import BaseCommand, CommandError
from movieapi.models import Movie, Actor
import codecs
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
        if not line or line[0] == '"':
            # It's a serie entry or invalid line, skip
            return None, None
        else:
            line = line.strip()
            year = line[-4:]
            if year == '????':
                year = 0
            stripped = line[:-4].strip()
            pieces = line.split('(')
            title = pieces[0].strip()
            return title, year

    def import_movies(self, filename):
        in_body = False  # Denotes if we are done skipping the file heading
        movies = []
        counter = 0
        progress = 0
        #f = codecs.open(filename, encoding='utf-8')
        f = codecs.open(filename, encoding='ISO-8859-1')
        for line in f:
            #if not in_body and 'MOVIES LIST' in line:
            if not in_body and '===========' in line:
                in_body = True
                continue

            if in_body:
                title, year = self.parse_movie_line(line)
                #if title:
                #    self.stdout.write(title)
                if title:
                    movies.append({'title': title, 'year': year})
                    #movie = Movie(title=title, year=year)
                    #movie.save()
                    counter += 1
                    progress += 1
                    if progress == 1000:
                        self.stdout.write(str(counter))
                        progress = 0
        return movies

    def handle(self, *args, **options):
        self.stdout.write('Importing IMDb files from "%s"' % options['directory'])


        movies_file = os.path.join(options['directory'], 'movies.list')
        self.stdout.write('Processing ' + movies_file)
        if os.path.isfile(os.path.join(options['directory'], 'movies.list')):
            #Movie.objects.all().delete()
            movies = self.import_movies(movies_file)
        else:
            self.stderr.write(movies_file + ' not found')
            return 1
