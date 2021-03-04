from django import forms
from .models import Search


class Inputform(forms.ModelForm):
    
    class Meta:
        model = Search
        fields = ("search_term", "no_of_terms")
        

