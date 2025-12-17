from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
import uuid

# Create your models here.
class CustomUserManager(UserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required")

        user = self.model(
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(username, password, **extra_fields)



class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user_ref_uid = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True
    )
    username = models.CharField(
        max_length=255,
        unique=True
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )

    # Basic Identity
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    other_name = models.CharField(max_length=255, blank=True, null=True)

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)

    gender = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female")],
        blank=True,
        null=True,
    )
    date_of_birth = models.DateField(blank=True, null=True)

    address = models.TextField(blank=True, null=True)

    profile_photo = models.ImageField(
        upload_to="staff/photos/", blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

#customer care staff profile can be added later
# class CustomerCareProfile(models.Model):
#     user = models.OneToOneField(
#         User, on_delete=models.CASCADE, related_name="staff_profile"
#     )
