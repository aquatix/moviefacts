from django.contrib import admin
from movieapi.models import Movie, Actor


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'year',)

    #def delete_everything(self):
    #    Movie.objects.all().delete()


admin.site.register(Movie, MovieAdmin)
