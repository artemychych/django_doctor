from unicodedata import category
from django.urls import re_path, include, path
from . import views
from rest_framework import routers


urlpatterns = [
    path('login', views.login),
    path('signup', views.signup),
    path('category', views.getCategories),
    path('category/<int:category_id>', views.getCategoryById),
    path('slider', views.getSliders),
    path('slider/<int:slider_id>', views.getSliderById),
    path('hospital', views.getHospitals),
    path('hospital/<int:hospital_id>', views.getHospitalById),
    path('doctor', views.getDoctors),
    path('doctor/<int:doctor_id>', views.getDoctorById),
    path('hospital/doctors/<int:hospital_id>', views.getHospitalDoctors),
    path('appointment', views.createAppointment),
    path('appointment/user/<int:user_id>', views.getUserAppointments),
    path('doctor/category/<int:category_id>', views.getDoctorsByCategory)
]

