from django.shortcuts import get_object_or_404
from django_filters import CharFilter, FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, serializers, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from materials.models import Course
from materials.permissions import ThreeTierAccessPermission
from materials.services import create_price, create_session, retrieve_session
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


class PaymentsCreateView(generics.CreateAPIView):
    """Контроллер для создания платежа и сессии Stripe."""

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(owner=self.request.user)
        course = payment.course_payment

        if not course.stripe_course_id or not course.price:
            payment.delete()
            raise serializers.ValidationError(
                {"error": "Курс не настроен для оплаты (нет ID Stripe или цены)."}
            )

        price_response = create_price(
            amount=course.price, product_id=course.stripe_course_id
        )

        if "id" not in price_response:
            payment.delete()
            raise serializers.ValidationError(
                {"stripe_error": "Не удалось создать цену Stripe."}
            )

        stripe_price_id = price_response["id"]

        success_url = (
            "http://127.0.0.1:8000/payments/success/?session_id={CHECKOUT_SESSION_ID}"
        )
        cancel_url = "http://127.0.0.1:8000/payments/cancel/"

        session_response = create_session(
            price_id=stripe_price_id, success_url=success_url, cancel_url=cancel_url
        )
        if "url" not in session_response:
            payment.delete()
            raise serializers.ValidationError(
                {"stripe_error": "Не удалось создать сессию оплаты Stripe."}
            )
        payment.link_to_the_payment = session_response["url"]
        payment.stripe_session_id = session_response["id"]
        payment.save()


class PaymentSuccessView(generics.RetrieveAPIView):
    """
    Проверяет статус оплаты Stripe, отмечает платеж как завершенный
    и активирует подписку на курс.
    """

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get("session_id")

        if not session_id:
            return Response(
                {"error": "Отсутствует ID сессии Stripe."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            payment = Payments.objects.get(stripe_session_id=session_id)
        except Payments.DoesNotExist:
            return Response(
                {"error": "Платеж не найден."}, status=status.HTTP_404_NOT_FOUND
            )

        if payment.owner != request.user:
            return Response(
                {"error": "У вас нет прав на просмотр этого платежа."},
                status=status.HTTP_403_FORBIDDEN,
            )

        session_data = retrieve_session(session_id)

        if session_data.get("payment_status") == "paid":
            if not payment.is_paid:
                payment.is_paid = True
                payment.save()
                course = payment.course_payment
                user = payment.owner
                Subscription.objects.get_or_create(user=user, course=course)

                message = f"Оплата успешно завершена. Подписка на курс '{course.name}' активирована!"
            else:
                message = (
                    "Платеж уже был отмечен как завершенный ранее. Подписка активна."
                )

            return Response({"message": message}, status=status.HTTP_200_OK)

        else:
            return Response(
                {"message": "Платеж не завершен. Пожалуйста, повторите попытку."},
                status=status.HTTP_200_OK,
            )


class PaymentCancelView(generics.RetrieveAPIView):
    """Представление для обработки отмены оплаты."""

    def get(self, request, *args, **kwargs):
        return Response(
            {"message": "Оплата отменена пользователем."},
            status=status.HTTP_400_BAD_REQUEST,
        )
