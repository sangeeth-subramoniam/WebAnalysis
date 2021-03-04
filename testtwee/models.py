from django.db import models

# Create your models here.

class Search(models.Model):
    search_term = models.CharField(max_length=50)
    no_of_terms = models.IntegerField(default=20)

    def __str__(self):
        return self.search_term
    
