from django_filters import FilterSet, CharFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from users.models import Payments
from users.serializers import PaymentSerializer


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

    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = [
        "date_payment",
    ]
