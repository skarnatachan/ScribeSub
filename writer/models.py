from django.db import models
from django.conf import settings


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    is_premium = models.BooleanField(default=False, verbose_name="Is premium?")
    article2customuser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customuser2article',
        null=True,
    )

    def __str__(self):
        return self.title
