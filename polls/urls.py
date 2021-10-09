from django.urls import path
from cauth.views import AuthOnly
from . import views

urlpatterns = [
    path('', AuthOnly(views.index), name='index'),
]