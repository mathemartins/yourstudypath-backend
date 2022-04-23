from django.db import models
from django_countries.fields import CountryField


# Create your models here.
class CourseOfStudy(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "course_of_study"
        verbose_name = "Course Of Study"
        verbose_name_plural = "Course Of Study"

    def __str__(self):
        return self.name


class University(models.Model):
    name = models.CharField(max_length=200)
    country_location = CountryField(default='NG')
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "university"
        verbose_name = "University"
        verbose_name_plural = "University"

    def __str__(self):
        return self.name
