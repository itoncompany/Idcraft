from django.urls import path
from MainApps import views

urlpatterns = [
    path('', views.home, name='home'),
    path('school-dashboard/', views.school_dashboard, name='school_dashboard'),
    path('service-pricing/', views.service_pricing, name='service_pricing'),
    path('grade-list/', views.grade_list, name='grade_list'),
    path('card-form/<str:class_id>/', views.card_form, name='card_form'),
    path('student/add/', views.add_student, name='add_student'),  # NEW
    path('student/<int:pk>/edit/', views.edit_student, name='edit_student'),
    path('student/<int:pk>/delete/', views.delete_student, name='delete_student'),
]
