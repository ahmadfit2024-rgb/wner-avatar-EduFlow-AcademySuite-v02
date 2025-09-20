from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom User Model that extends Django's AbstractUser.
    It adds a 'role' field to implement Role-Based Access Control (RBAC).
    """
    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        SUPERVISOR = 'supervisor', 'Supervisor'
        INSTRUCTOR = 'instructor', 'Instructor'
        STUDENT = 'student', 'Student'
        THIRD_PARTY = 'third_party', 'Third-Party Client'

    # The 'role' field is crucial for the entire system's permission logic.
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.STUDENT,
        help_text="The role of the user within the system."
    )

    # Adding full_name for convenience, as first_name and last_name can be cumbersome.
    full_name = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="User's full name."
    )
    
    # You can add other profile fields here if needed, like avatar, bio, etc.
    # For this project, profile info will be handled in a separate collection/model
    # or as an embedded document if using MongoDB extensively.

    def save(self, *args, **kwargs):
        # Automatically populate full_name from first and last names if it's empty
        if not self.full_name and (self.first_name or self.last_name):
            self.full_name = f"{self.first_name} {self.last_name}".strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username