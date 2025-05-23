from django.db import models

class Categories(models.Model):
    id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=255)  
    slug = models.SlugField(unique=True)  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.name