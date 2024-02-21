from api import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("posts", views.PostViewSet, basename="posts")
router.register("authors", views.AuthorViewSet, basename="authors")
router.register("tags", views.TagViewSet, basename="tags")

app_name = "api"
urlpatterns = [
    path("", include(router.urls))
]
