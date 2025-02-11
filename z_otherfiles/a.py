from django.contrib import admin
from encrypt_app import views
from django.urls import path,include

urlpatterns = [
    path("", views.encrypt_home,name="encrypt_home"),
    
]

# uu

from django.shortcuts import render
from django.conf import settings

# Create your views here.
def encrypt_home(request):
    return render(request, 'encryption.html')

# def encrypt_img(request):
#     return render(request, 'encryption.html')
