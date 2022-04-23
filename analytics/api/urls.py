from django.urls import path

from analytics.api.views import AnalyticsListAPIView

urlpatterns = [
    path('list/', AnalyticsListAPIView.as_view(), name='list'),
]
