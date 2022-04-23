from django.contrib import admin
from core.models import CourseOfStudy, University


# Register your models here.

@admin.register(CourseOfStudy)
class CourseOfStudyAdmin(admin.ModelAdmin):
    list_display = ('name', 'timestamp', 'updated')
    list_display_links = ('name',)
    search_fields = ('name',)


@admin.register(University)
class UniversityModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'country_location', 'timestamp', 'updated')
    list_display_links = ('name',)
    list_filter = ('country_location',)
    search_fields = ('name',)
