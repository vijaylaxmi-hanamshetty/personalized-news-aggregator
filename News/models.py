from django.db import models


class News(models.Model):
    id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=255)  
    url = models.URLField(max_length=500)
    category = models.CharField(max_length=100)  
    language = models.CharField(max_length=50)  
    logo_url = models.URLField(max_length=500, blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.name