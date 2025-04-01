from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, age, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            age=age
        )
        user.set_password(password)  # Hash password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, age, password=None):
        user = self.create_user(
            email=email,
            name=name,
            age=age,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Password will be hashed
    age = models.IntegerField()

    # User authentication-related fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # The following are necessary for Django's auth system
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'age']  # Fields required when creating superuser

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = "all_users"



class Golfer(models.Model):
    name = models.CharField(max_length=100)
    day_1_score = models.IntegerField()
    day_2_score = models.IntegerField()
    day_3_score = models.IntegerField()
    day_4_score = models.IntegerField()
    average_scores_dayoverday = models.FloatField(null=True, blank=True)
    tier = models.IntegerField()
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "all_golfers"