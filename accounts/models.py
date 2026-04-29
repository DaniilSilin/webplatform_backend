from django.db import models

from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    is_profile_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username