from rest_framework import serializers

from accounts.models import PreparingExam


class ExamSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField(read_only=True)
    course_of_study = serializers.SerializerMethodField()
    university = serializers.SerializerMethodField()

    class Meta:
        model = PreparingExam
        fields = [
            'exam_name',
            'exam_image',
            'exam_code',
            'students',
            'count',
            'course_of_study',
            'university',
        ]

    def get_count(self, obj: PreparingExam):
        return obj.students.all().count()

    def get_course_of_study(self, obj: PreparingExam):
        return obj.course_of_study.name

    def get_university(self, obj: PreparingExam):
        return obj.university.name
