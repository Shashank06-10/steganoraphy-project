from django.contrib import admin
from morse_code_app import views
from django.urls import path,include

urlpatterns = [
    path("enc/", views.encrypt,name="encrypt"),
    path("dec/", views.decrypt, name="decrypt"),

   
]