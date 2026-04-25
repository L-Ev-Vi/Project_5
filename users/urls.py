from django.urls import path
from rest_framework.routers import DefaultRouter

from users import views

from .apps import UsersConfig

router = DefaultRouter()
router.register(r"users", views.UserViewSet, basename="users")

app_name = UsersConfig.name

urlpatterns = [
    #Payments
    path("payments/", views.PaymentsListViewAPI.as_view(), name="payments"),
    path("payments/create/", views.PaymentsCreateViewAPI.as_view(), name="payments_create"),
    path("payments/retrieve/<int:pk>/", views.PaymentsRetrieveViewAPI.as_view(), name="payments_retrieve"),

    # path("users/update/<int:pk>/", views.UserUpdateViewAPI.as_view(), name="users_update"),
    # path("users/destroy/<int:pk>/", views.UserDestroyViewAPI.as_view(), name="users_destroy"),
] + router.urls
