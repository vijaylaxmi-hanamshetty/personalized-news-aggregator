from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone, name, role, password=None):
        if not phone:
            raise ValueError("Users must have a phone number")
        user = self.model(phone=phone, name=name, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    ROLE_USER = "user"
    ROLE_ADMIN = "admin"

    ROLE_CHOICES = (
        (ROLE_USER, "User"),
        (ROLE_ADMIN, "Admin"),
    )

    phone = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default=ROLE_USER)
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["name", "role"]

    objects = UserManager()

    def __str__(self):
        return f"{self.name} ({self.role})"
