from django.contrib import admin
from .models import *

class Filter(admin.ModelAdmin):
    list_display = ('id', 'name', 'director', 'release_date')
    list_filter = ('director', 'genres')



# Register your models here.
admin.site.site_header = 'Django Movies'
admin.site.register(Movie, Filter)
admin.site.register(Review)
admin.site.register(Genre)
