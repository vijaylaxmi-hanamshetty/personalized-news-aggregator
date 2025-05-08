from django.db import models
from News.models import News
from Categories.models import Categories

class Articles(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    summary = models.TextField(blank=True, null=True)
    url = models.URLField()
    published_at = models.DateTimeField()
    source = models.ForeignKey(News, on_delete=models.CASCADE, related_name="articles")
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="articles")
    language = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title