from rest_framework import serializers

from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["name", "description", "preview", "link_to_the_video", "course"]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    @staticmethod
    def get_lesson_count(instance):
        return instance.lessons.count()

    class Meta:
        model = Course
        fields = ["name", "description", "preview", "lesson_count", "lessons"]
