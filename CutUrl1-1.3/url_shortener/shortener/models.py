from django.db import models
from django.contrib.auth.models import User

class URL(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.original_url



