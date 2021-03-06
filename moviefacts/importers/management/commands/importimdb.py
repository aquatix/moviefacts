from django.core.management.base import BaseCommand, CommandError
from movieapi.models import Movie, Actor
import base64
import codecs
import os
import re

class Command(BaseCommand):
    help = 'Import the imdb files from the specified directory'

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str)

    def movie_hash(title, year):
        h = hashlib.md5(str(year) + base64.encodestring(title.encode('utf-8')))
        return h.digest().encode('base64')

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

    def parse_movie_rating_line(self, line):
        # Movies:
        # Se7en (1995)                                            1995
        #       0000001321  463629   8.0  Groundhog Day (1993)

        # Series (skip):
        # "Family Guy" (1999)                                     1999-????
        # "Family Guy" (1999) {8 Simple Rules for Buying My Teenage Daughter (#4.8)}      2005
        line = line.strip()
        if not line:
            # It's a serie entry or invalid line, skip
            return None, None, None, None
        else:
            pieces = line.split('  ')
            title = pieces[-1]
            if title and title[0] == '"' or '(VG)' in title:
                # It's a serie entry or Video Game, skip
                return None, None, None, None
            votes = pieces[-3].strip()
            rating = float(pieces[-2].strip())
            title = title.replace(' (V)', '').replace(' (TV)', '')
            try:
                year = int(title[-5:-1])
            except ValueError:
                # Year could not be extracted, bail for now
                return None, None, None, None
            title = title[:-6].strip()
            #print title
            if year == '????':
                year = 0
            return title, year, rating, votes

    def import_movies(self, filename):
        in_body = False  # Denotes if we are done skipping the file heading
        movies = {}
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
                    movies[str(year) + base64.encodestring(title.encode('utf-8'))] = {'title': title, 'year': year}
                    #movie = Movie(title=title, year=year)
                    #movie.save()
                    counter += 1
                    progress += 1
                    if progress == 1000:
                        self.stdout.write(str(counter))
                        progress = 0
        return movies

    def import_runningtimes(self, filename):
        """ Needs fixing """
        in_body = False  # Denotes if we are done skipping the file heading
        movies = {}
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
                title, year, runtime = self.parse_movie_runtime_line(line)
                #if title:
                #    self.stdout.write(title)
                if title:
                    movies[str(year) + base64.encodestring(title.encode('utf-8'))] = {'title': title, 'year': year}
                    #movie = Movie(title=title, year=year)
                    #movie.save()
                    counter += 1
                    progress += 1
                    if progress == 1000:
                        self.stdout.write(str(counter))
                        progress = 0
        return movies

    def import_movies_with_ratings(self, filename):
        in_body = False  # Denotes if we are done skipping the file heading
        movies = {}
        counter = 0
        progress = 0
        f = codecs.open(filename, encoding='ISO-8859-1')
        for line in f:
            if not in_body and 'New  Distribution  Votes  Rank  Title' in line:
                if counter > 1:
                    # There's two of those headings...
                    in_body = True
                    counter = 0
                else:
                    counter += 1
                continue

            if in_body:
                if '------------------------------------------------------------------------------' in line:
                    break
                title, year, rating, votes = self.parse_movie_rating_line(line)
                if title:
                    #print(title, year, rating, votes)
                    try:
                        movies[str(year) + base64.encodestring(title.encode('utf-8'))] = {'title': title, 'year': year, 'rating': rating, 'votes': votes}
                    except UnicodeEncodeError as e:
                        print "FAIL"
                        print title
                        sys.exit()
                    #movie = Movie(title=title, year=year)
                    #movie.save()
                    counter += 1
                    progress += 1
                    if progress == 1000:
                        self.stdout.write(str(counter))
                        progress = 0
        return movies

    def import_plots(self, filename, movies):
        """ Enrich the movies list with plot info """
        in_body = False  # Denotes if we are done skipping the file heading
        in_plot = False  # Denotes if we are in a plot entry
        plot = ''
        movies = {}
        counter = 0
        progress = 0
        f = codecs.open(filename, encoding='ISO-8859-1')
        for line in f:
            if not in_body and '===================' in line:
                in_body = True
                continue

            if in_body:
                if line[:3] == 'MV:':
                    title, year, runtime = self.parse_movie_runtime_line(line)
                if title:
                    movies[str(year) + base64.encodestring(title.encode('utf-8'))] = {'title': title, 'year': year}
                    #movie = Movie(title=title, year=year)
                    #movie.save()
                    counter += 1
                    progress += 1
                    if progress == 1000:
                        self.stdout.write(str(counter))
                        progress = 0
        return movies

    def movie_languages(self, filename, movies):
        return movies

    def handle(self, *args, **options):
        self.stdout.write('Importing IMDb files from "%s"' % options['directory'])


        movies_file = os.path.join(options['directory'], 'movies.list.tsv')
        self.stdout.write('Processing ' + movies_file)




        movies_file = os.path.join(options['directory'], 'movies.list')
        self.stdout.write('Processing ' + movies_file)
        #if os.path.isfile(os.path.join(options['directory'], 'movies.list')):
        #    #Movie.objects.all().delete()
        #    movies = self.import_movies(movies_file)
        #else:
        #    self.stderr.write(movies_file + ' not found')
        #    return 1

        movies_file = os.path.join(options['directory'], 'ratings.list')
        if os.path.isfile(movies_file):
            movies = self.import_movies_with_ratings(movies_file)
        else:
            self.stderr.write(movies_file + ' not found')
            return 1

        self.stdout.write('Importing languages')
        languages_file = os.path.join(options['directory'], 'language.list')
        if os.path.isfile(movies_file):
            movies = self.movie_languages(languages_file, movies)
        else:
            self.stderr.write(languages_file + ' not found')
            return 1

        self.stdout.write('Done reading, save to database...')

        self.stdout.write('First remove all old movies...')
        Movie.objects.all().delete()

        self.stdout.write('Done cleaning, save to database...')

        counter = 1
        progress = 1
        for key in movies:
            movie = movies[key]
            Movie.objects.create(title=movie['title'], year=movie['year'], rating=movie['rating'], votes=movie['votes'])
            counter += 1
            progress += 1
            if progress == 1000:
                self.stdout.write(str(counter))
                progress = 1

        self.stdout.write('Done saving to database, action!')
