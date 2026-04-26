from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import views

from .apps import UsersConfig

router = DefaultRouter()
router.register(r"users", views.UserViewSet, basename="users")

app_name = UsersConfig.name

urlpatterns = [
    # Payments
    path("payments/", views.PaymentsListViewAPI.as_view(), name="payments"),
    path("payments/create/", views.PaymentsCreateViewAPI.as_view(), name="payments_create"),
    path("payments/retrieve/<int:pk>/", views.PaymentsRetrieveViewAPI.as_view(), name="payments_retrieve"),
    # User
    path("users/token/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="token_obtain_pair"),
    path("users/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
] + router.urls
