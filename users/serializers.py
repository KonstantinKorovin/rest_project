from rest_framework import serializers

from materials.serializers import CourseSerializer
from users.models import Payments


class PaymentSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = Payments
        fields = "__all__"
