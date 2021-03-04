from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request , 'homepage.htm')


def contact(request):
    return render(request , 'contact.htm')

def about(request):
    return render(request , 'about.htm')