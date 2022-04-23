from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from analytics.api.serializers import AnalyticsDataSerializer
from analytics.models import CourseViewEvent


class AnalyticsListAPIView(generics.ListAPIView):
    queryset = CourseViewEvent.objects.all()
    serializer_class = AnalyticsDataSerializer
    authentication_classes = [SessionAuthentication, JWTAuthentication]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request
        user = request.user
        if not user.is_authenticated:
            return CourseViewEvent.objects.none()
        return qs.filter(user=request.user)