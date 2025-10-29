from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.paginators import CourseLessonPaginator
from materials.permissions import ThreeTierAccessPermission
from materials.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    pagination_class = CourseLessonPaginator
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, ThreeTierAccessPermission]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ListLessons(generics.ListAPIView):
    pagination_class = CourseLessonPaginator
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ThreeTierAccessPermission]


class CreateLesson(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ThreeTierAccessPermission]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RetrieveLesson(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ThreeTierAccessPermission]


class UpdateLesson(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ThreeTierAccessPermission]


class DestroyLesson(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ThreeTierAccessPermission]
