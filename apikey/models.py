from django.db import models


class APIKey(models.Model):
    user = models.CharField(max_length=100)
    key = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user