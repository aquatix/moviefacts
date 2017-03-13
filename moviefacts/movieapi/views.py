from django.shortcuts import render
from rest_framework import viewsets
from movieapi.serializers import MovieSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from movieapi.models import Movie
from random import randint


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class RandomMovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    #filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    def get_queryset(self):
        movies = Movie.objects.all()
        print self.kwargs
        try:
            year = self.kwargs['year']
            print year
            movies = movies.filter(year=year)
        except:
            pass
        count = movies.count()
        random_index = randint(0, count - 1)
        return [movies[random_index]]
