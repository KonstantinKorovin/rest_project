from django.urls import path

from users.apps import UsersConfig
from users.views import PaymentsList

app_name = UsersConfig.name


urlpatterns = [
    path("payments/", PaymentsList.as_view(), name="list-payments"),
    #  --  #
]
