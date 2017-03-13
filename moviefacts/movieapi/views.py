from django.shortcuts import render
from rest_framework import viewsets
from movieapi.serializers import MovieSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from movieapi.models import Movie


class MovieViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Movie.objects.all().order_by('-date_joined')
    serializer_class = MovieSerializer


class RandomMovieView(APIView):
    def get(self, request, format=None):
        """
        Return a random movie
        """
        count = Movie.objects.all().count()
        random_index = randint(0, count - 1)
        return Movie.objects.all()[random_index]
