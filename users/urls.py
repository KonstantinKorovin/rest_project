from django.urls import path

from users.apps import UsersConfig
from users.views import MyTokenObtainPairView, PaymentsList

app_name = UsersConfig.name


urlpatterns = [
    path("payments/", PaymentsList.as_view(), name="list-payments"),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    #  --  #
]
