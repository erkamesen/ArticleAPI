from api import views
from django.urls import path


app_name = "api"
urlpatterns = [

    path('', view=views.PostAPIView.as_view(), name="posts"),
    path('tags/', view=views.TagAPIView.as_view(), name="tags"),
    path('authors/', view=views.AuthorAPIView.as_view(), name="authors"),


    path('<int:pk>/', view=views.PostDetailAPIView.as_view(),
         name="posts-detail"),

    path('tags/<int:pk>/', view=views.TagDetailAPIView.as_view(),
         name="tags-detail"),

    path('authors/<int:pk>/',
         view=views.AuthorDetailAPIView.as_view(),
         name="authors-detail"),
]
