from django.urls import path,include
from . import views

app_name = 'homepage'
urlpatterns = [
    path('', views.home , name = "home"),
    path('contact', views.contact , name = "contact"),
    path('about', views.about , name = "about"),

    
]