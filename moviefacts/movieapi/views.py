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


#class RandomMovieViewSet(viewsets.ModelViewSet):
#    count = Movie.objects.all().count()
#    random_index = randint(0, count - 1)
#    queryset = Movie.objects.all()[random_index]
#    serializer_class = MovieSerializer
