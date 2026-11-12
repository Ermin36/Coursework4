from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Create your models here.
class CustomManagerUser(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff', False) is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser', False) is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    image = models.ImageField(default='default.jpeg', upload_to='images/', blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)

    objects = CustomManagerUser()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email