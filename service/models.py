from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


# Create your models here.
class UserManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError("User must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create a new superuser profile"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class User(AbstractUser):
    """Database model for users in the system"""

    username = None
    email = models.EmailField(max_length=255, unique=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        """Return string representation of our user"""
        return self.email


class Service(models.Model):
    title = models.CharField()

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return self.title


class ServiceRequest(models.Model):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="requests"
    )
    task = models.ForeignKey(
        Task, blank=True, null=True, on_delete=models.CASCADE, related_name="requests"
    )
    worker = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL, related_name="requests"
    )
