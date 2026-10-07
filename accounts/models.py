from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    hostel_location = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="e.g., Hall 1, Main Campus, or Off-Campus"
    )

    def __str__(self):
        return f"{self.username} ({self.email if self.email else 'No Email'})"