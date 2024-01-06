from __future__ import annotations
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(
        self, email: str, password: str | None = None, **other_fields
    ) -> User: 
        user = User(email=email, **other_fields)
        
        if password: 
            user.set_password(password)
        else:
            user.set_unusable_password()
            
        user.save()
        return user
    
    def create_superuser(self, email: str, password: str | None = None, **other_fields) -> User:
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)
        
        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")
        
        return self.create_user(email, password, **other_fields)
    
    

class User(AbstractUser):

    # remove default fields
    first_name = None
    last_name = None

    email: str = models.EmailField("Email Address", unique=True)
    username: str = models.CharField(max_length=60)
    bio: str = models.TextField(blank=True)
    image: str | None = models.URLField(null=True, blank=True)

    followers = models.ManyToManyField("self", blank=True, symmetrical=False)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()


    def get_full_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else: 
            return self.username
       

    def get_short_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}{self.last_name}"
        else:
            return self.username
