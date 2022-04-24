import random
from itertools import chain

from django.views.generic import RedirectView
from rest_framework import generics, status
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from analytics.models import CourseViewEvent
from courses.api.serializers import CourseSerializer
from courses.models import Course, Lecture

from videos.mixins import MemberRequiredMixin
from yourstudypath.mixins import StaffEditorPermissionMixin


class CourseCreateAPIView(StaffEditorPermissionMixin, generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [SessionAuthentication, JWTAuthentication]

    def perform_create(self, serializer):
        serializer.partial = True
        serializer.save(user=self.request.user)


class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [SessionAuthentication, JWTAuthentication]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if not user.is_authenticated:
            return Course.objects.none()
        mod_qs = list(chain(qs.owned(user)))  # can accept multiple qs and chain them together as one
        return mod_qs  # .filter(user=request.user)


class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    lookup_field = 'slug'

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        qs = Course.objects.filter(slug=slug).lectures().owned(self.request.user)  # returns lecture lists
        if qs.exists():
            obj = qs.first()
            if self.request.user.is_authenticated:
                view_event, created = CourseViewEvent.objects.get_or_create(user=self.request.user, course=obj)
                if view_event:
                    view_event.views += 1
                    view_event.save()
            return obj
        raise Http404


class CoursePurchaseAPIView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]

    def get(self, request, slug=None):
        qs = Course.objects.filter(slug=slug).owned(self.request.user)
        if qs.exists():
            user = self.request.user
            if user.is_authenticated:
                my_courses = user.mycourses
                # run transaction
                # create user into paystack account for ysp
                # charge user
                # if transaction successful:
                my_courses.courses.add(qs.first())
                return qs.first().get_absolute_url()
            return qs.first().get_absolute_url()
        return "/courses/"


class LectureDetailAPIView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]

    def get(self, request, cslug=None, lslug=None, *args, **kwargs):
        obj = None
        qs = Course.objects.filter(slug=cslug).lectures().owned(request.user)
        if not qs.exists():
            raise Http404
        course_: Course = qs.first()
        if request.user.is_authenticated:
            view_event, created = CourseViewEvent.objects.get_or_create(user=request.user, course=course_)
            if view_event:
                view_event.views += 1
                view_event.save()

        lectures_qs = course_.lecture_set.filter(slug=lslug)
        if not lectures_qs.exists():
            raise Http404

        obj: Lecture = lectures_qs.first()

        if not course_.is_owner and not obj.free:  # and not user.is_member:
            return Response(
                {"message": "You are not a eligible to watch this course"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
            {
                "message": "success",
                "data": {
                    "lecture": obj.title,
                    "lecture_order_number": obj.order,
                    "lecture_slug": obj.slug,
                    "is_lecture_free": obj.free,
                    "lecture_description": obj.description,
                    "lecture_video": obj.video.embed_code,
                    "lecture_timestamp": obj.timestamp,
                    "lecture_updated": obj.updated,
                    "course": course_.title,
                    "course_description": course_.description
                }
            },
            status=status.HTTP_200_OK
        )


class CourseRUDAPIView(StaffEditorPermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    lookup_field = 'slug'

    def perform_update(self, serializer):
        serializer.partial = True
        if not self.request.user.is_staff:
            return Response({"detail": "Must be a staff of YSP"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer.save()

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        obj = Course.objects.filter(slug=slug)
        if obj.exists():
            return obj.first()
        raise Http404
