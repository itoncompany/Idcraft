from django.urls import path
from Authentications import views
urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
      path("signup/", views.signup_view, name="signup"),
    path("signin/", views.signin_view, name="signin"),
]
