from django_filters import CharFilter, FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from materials.permissions import ThreeTierAccessPermission
from users.models import Payments
from users.serializers import MyTokenObtainPairSerializer, PaymentSerializer


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
