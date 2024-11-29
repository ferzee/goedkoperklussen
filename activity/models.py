from django.db import models


class Activity(models.Model):
    is_active = models.BooleanField(default=True)
    activity_name = models.CharField(max_length=255)
    activity_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.activity_name

    class Meta:
        verbose_name_plural = "Activities"
