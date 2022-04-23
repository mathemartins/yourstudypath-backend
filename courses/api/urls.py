from django.urls import path

from courses.api.views import CourseListCreateAPIView

urlpatterns = [
    path('list-create/', CourseListCreateAPIView.as_view(), name='list-create'),
]
