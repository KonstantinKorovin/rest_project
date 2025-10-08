from django.urls import path

from users.apps import UsersConfig
from users.views import MyTokenObtainPairView, PaymentsList, UserCreate, UserProfileView

app_name = UsersConfig.name


urlpatterns = [
    path("payments/", PaymentsList.as_view(), name="list-payments"),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("register/", UserCreate.as_view(), name="create-user"),
    path("my/profile/", UserProfileView.as_view(), name="my-profile"),
    #  --  #
]
