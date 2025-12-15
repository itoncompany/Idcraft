from django.urls import path
from Authentications import views
urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
]
