from knox import views as KnoxViews
from authentication.views import LoginView, RegisterView
from django.urls import path

app_name = "auth"
urlpatterns = [
    path('login/', LoginView.as_view(), name="knox-login"),
    path('logout/', KnoxViews.LogoutView.as_view(), name="knox-logout"),
    path('logoutall/', KnoxViews.LogoutAllView.as_view(), name="knox-logoutall"),
    path('register/', RegisterView.as_view(), name="knox-register"),
]
