from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField(max_length=100, primary_key=True)
    user_name = models.CharField(max_length=100, unique=True)
    password_SHA256 = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    last_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    joining_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email