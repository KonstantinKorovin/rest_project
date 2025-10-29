from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import (
    CourseViewSet,
    CreateLesson,
    DestroyLesson,
    ListLessons,
    RetrieveLesson,
    UpdateLesson,
)

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r"", CourseViewSet, basename="")


urlpatterns = [
    path("lesson/create/", CreateLesson.as_view(), name="create-lesson"),
    path("lessons/", ListLessons.as_view(), name="list-lessons"),
    path("lesson/<int:pk>/detail/", RetrieveLesson.as_view(), name="detail-lesson"),
    path("lesson/<int:pk>/update/", UpdateLesson.as_view(), name="update-lesson"),
    path("lesson/<int:pk>/delete/", DestroyLesson.as_view(), name="delete-lesson"),
] + router.urls
