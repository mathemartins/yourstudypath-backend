from django.contrib.auth import get_user_model
from django.db import models
from courses.models import Course

User = get_user_model()


class CourseViewEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.views)
