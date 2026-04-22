from django.urls import path
from rest_framework.routers import DefaultRouter

from materials import views

from .apps import MaterialsConfig

router = DefaultRouter()
router.register(r"course", views.CourseViewSet, basename="course")

app_name = MaterialsConfig.name

urlpatterns = [
    path("lessons/", views.LessonListViewAPI.as_view(), name="lessons"),
    path("lesson/create/", views.LessonCreateViewAPI.as_view(), name="lesson_create"),
    path("lesson/retrieve/<int:pk>/", views.LessonRetrieveViewAPI.as_view(), name="lesson_retrieve"),
    path("lesson/update/<int:pk>/", views.LessonUpdateViewAPI.as_view(), name="lesson_update"),
    path("lesson/destroy/<int:pk>/", views.LessonDestroyViewAPI.as_view(), name="lesson_destroy"),
] + router.urls
