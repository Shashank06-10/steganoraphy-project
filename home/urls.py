from django.contrib import admin
from django.urls import path
from home import views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index,name="home"),
    path("about", views.about,name="about"),
    path("contactus", views.contactus,name="contactus"),
    path('SecureEncrypt/',  views.secureencrypt,name="secureencrypt"),
    path('SecureEncrypt/image/', include('image_app.urls')),
    path('SecureEncrypt/emoji/', include('emoji_app.urls')),
    path('SecureEncrypt/audio/', include('audio_app.urls')),
    path('SecureEncrypt/video/', include('video_app.urls')),
    path('SecureEncrypt/morsecode/', include('morse_code_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])