from django.db import models
from User.models import User
import secrets
# Create your models here.

class Token(models.Model):
    user = models.OneToOneField(User, models.CASCADE, primary_key=True)
    token = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email