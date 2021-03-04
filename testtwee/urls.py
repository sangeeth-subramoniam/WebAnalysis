from django.urls import path,include
from . import views

app_name = 'testtwee'
urlpatterns = [
    path('', views.index , name = "testtweeindex"),

]