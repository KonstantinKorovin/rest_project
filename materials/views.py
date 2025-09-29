from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class ListLessons(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class CreateLesson(generics.CreateAPIView):
    serializer_class = LessonSerializer


class RetrieveLesson(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class UpdateLesson(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class DestroyLesson(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
