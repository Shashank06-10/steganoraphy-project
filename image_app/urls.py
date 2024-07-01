from django.contrib import admin
from image_app import views
from django.urls import path,include

urlpatterns = [
    path("enc/", views.encrypt,name="encrypt"),
    path("dec/", views.decrypt,name="decrypt"), 
      
    path("enc/encresult/", views.encresult, name="encresult"),
    path("enc/decresult/", views.decresult, name="decresult"),
    
]