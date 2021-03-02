from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'index'

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('account/<slug:user>', views.userAccount, name="userAccount"),
    path('account/<slug:user>/password_forgot', views.forgotPassword, name="forgotPassword"),
]
