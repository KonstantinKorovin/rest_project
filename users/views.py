from django.shortcuts import get_object_or_404
from django_filters import CharFilter, FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from materials.models import Course
from materials.permissions import ThreeTierAccessPermission
from users.models import Payments, Subscription
from users.serializers import (
    MyTokenObtainPairSerializer,
    PaymentSerializer,
    SubscriptionSerializer,
    UserProfile,
    UserSerializer,
)


class PaymentsFilter(FilterSet):
    course_name = CharFilter(field_name="course_payment__name", lookup_expr="icontains")
    lesson_name = CharFilter(field_name="lesson_payment__name", lookup_expr="icontains")

    class Meta:
        model = Payments
        fields = ["lesson_name", "course_name", "payment_method"]


class PaymentsList(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    filterset_class = PaymentsFilter
    permission_classes = [IsAuthenticated, ThreeTierAccessPermission]

    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = [
        "date_payment",
    ]


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfile
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class SubscriptionView(APIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course_id")
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
            http_status = status.HTTP_200_OK

        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"
            http_status = status.HTTP_201_CREATED

        return Response({"message": message}, status=http_status)
