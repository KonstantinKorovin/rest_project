from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from materials.serializers import CourseSerializer
from users.models import Payments


class PaymentSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = Payments
        fields = "__all__"


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["email"] = user.email
        return token
