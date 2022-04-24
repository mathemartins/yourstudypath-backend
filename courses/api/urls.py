from django.urls import path

from courses.api.views import (
    CourseCreateAPIView, CourseListAPIView, CourseDetailAPIView,
    CoursePurchaseAPIView, LectureDetailAPIView, CourseRUDAPIView
)

urlpatterns = [
    path('create/', CourseCreateAPIView.as_view(), name='create'),
    path('list/', CourseListAPIView.as_view(), name='list'),
    path('<slug>/', CourseDetailAPIView.as_view(), name='detail'),
    path('<slug>/purchase/', CoursePurchaseAPIView.as_view(), name='purchase'),
    path('<cslug>/<lslug>/', LectureDetailAPIView.as_view(), name='lecture-detail'),
    path('<slug>/edit-delete/', CourseRUDAPIView.as_view(), name='update-delete'),
]