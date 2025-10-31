from rest_framework import serializers

from materials.models import Course, Lesson
from materials.services import create_course
from materials.validators import UrlValidator
from users.models import Subscription


class LessonSerializer(serializers.ModelSerializer):
    link_to_the_video = serializers.CharField(validators=[UrlValidator()])

    class Meta:
        model = Lesson
        fields = ["name", "description", "preview", "link_to_the_video", "course"]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, course_obj):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return False

        user = request.user
        return Subscription.objects.filter(user=user, course=course_obj).exists()

    @staticmethod
    def get_lesson_count(instance):
        return instance.lessons.count()

    class Meta:
        model = Course
        fields = "__all__"

    def create(self, validated_data):
        stripe_response = create_course(
            course_name=validated_data["name"],
            description=validated_data.get("description"),
        )
        if "id" not in stripe_response:
            raise serializers.ValidationError(
                {"stripe_error": "Не удалось создать продукт в Stripe."}
            )

        validated_data["stripe_course_id"] = stripe_response["id"]
        course_instance = super().create(validated_data)
        return course_instance
