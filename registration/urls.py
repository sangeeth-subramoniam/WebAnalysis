from django.urls import path,include
from . import views

app_name = 'registration'
urlpatterns = [
    path('signup', views.signup , name = "signup"),
    path('signin', views.signin , name = "signin"),
    path('signout', views.signout , name = "signout"),

]
