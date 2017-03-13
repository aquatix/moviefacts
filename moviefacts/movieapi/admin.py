from django.contrib import admin
from movieapi.models import Movie, Actor


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'year',)


admin.site.register(Movie, MovieAdmin)
