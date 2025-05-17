from django.db import models
from django.conf import settings
from Articles.models import Articles

class SavedArticles(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_articles")
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name="saved_by_users")
    saved_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'article')
    def __str__(self):
        return f"{self.user.username} saved {self.article.title}"