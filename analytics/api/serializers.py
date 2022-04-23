from rest_framework import serializers

from analytics.models import CourseViewEvent


class AnalyticsDataSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    course = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CourseViewEvent
        fields = [
            'user',
            'course',
            'views',
            'updated',
        ]

    def get_user(self, obj: CourseViewEvent):
        return obj.user.username

    def get_course(self, obj: CourseViewEvent):
        return obj.course.title