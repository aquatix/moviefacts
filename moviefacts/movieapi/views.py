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

    def get_queryset(self):
        count = Movie.objects.all().count()
        random_index = randint(0, count - 1)
        return [Movie.objects.all()[random_index]]
        this_movie = Movie.objects.all()[random_index]
        return Movie.objects.filter(this_movie)
