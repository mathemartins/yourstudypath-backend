from django.urls import re_path, path

from core.api.views import ExamListAPIView

urlpatterns = [
    path('list/', ExamListAPIView.as_view()),
]