from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from materials.serializers import CourseSerializer
from users.models import CustomUser, Payments


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "phone_number", "city"]

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = CustomUser.objects.create_user(**validated_data, password=password)
        return user


class UserProfile(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "phone_number", "city", "avatar"]
        read_only_fields = fields
