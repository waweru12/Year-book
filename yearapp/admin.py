from django.contrib import admin
from .models import Project, Profile, Rating

class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ()

admin.site.register(Project)
admin.site.register(Profile)
admin.site.register(Rating)
