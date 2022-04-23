from django.shortcuts import render


# Create your views here.
from rest_framework import generics
from rest_framework.permissions import AllowAny

from accounts.models import PreparingExam
from core.api.serializers import ExamSerializer


class ExamListAPIView(generics.ListAPIView):
    queryset = PreparingExam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

