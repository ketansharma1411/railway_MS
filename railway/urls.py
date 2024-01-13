"""railway URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from rail import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signin/',views.signin),
    path('login/',views.login),
    path('train_info/',views.train_info),
    path('email_verify/',views.email_verification),
    path('seats_available/',views.check_seat_availability),
    path('book_seat/',views.booking_seats),
    #only made for validating user at booking seats--------------------
    path('demo_login/',views.demo_login), 
    path('test/',views.testing),
    #-----------------------------------------------------------------
    path('booking_history/',views.seat_history),
    path('forget_pass/',views.forget_password),
    path('reset_password/',views.reset_password),
    
]
