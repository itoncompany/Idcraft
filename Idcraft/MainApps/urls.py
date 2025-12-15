from django.urls import path
from MainApps import views


urlpatterns = [
    path('', views.home, name='home'),
    path('service-pricing/', views.service_pricing, name='service_pricing'),
]