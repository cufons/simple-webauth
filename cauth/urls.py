from django.urls import path

from . import views

urlpatterns = [
    path('', views.loginview, name='loginview'),
    path('fail/', views.loginfailed,name='loginfailed'),
    path('login/', views.login,name='login')
]