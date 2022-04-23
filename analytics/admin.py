from django.contrib import admin

# Register your models here.
from analytics.models import CourseViewEvent

admin.site.register(CourseViewEvent)