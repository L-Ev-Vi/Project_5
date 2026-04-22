from django.urls import path
from rest_framework.routers import DefaultRouter

from users import views

from .apps import UsersConfig

router = DefaultRouter()
router.register(r"users", views.UserViewSet, basename="users")

app_name = UsersConfig.name

urlpatterns = [
    # path("users/", views.UserListViewAPI.as_view(), name="users"),
    # path("users/create/", views.UserCreateViewAPI.as_view(), name="users_create"),
    # path("users/retrieve/<int:pk>/", views.UserRetrieveViewAPI.as_view(), name="users_retrieve"),
    # path("users/update/<int:pk>/", views.UserUpdateViewAPI.as_view(), name="users_update"),
    # path("users/destroy/<int:pk>/", views.UserDestroyViewAPI.as_view(), name="users_destroy"),
] + router.urls
