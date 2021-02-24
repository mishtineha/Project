from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User,AbstractUser
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class InvitationStatus(models.Model):
    status = models.CharField(max_length = 10,unique = True)

class Guest(models.Model):
    name = models.CharField(max_length = 10)
    email = models.EmailField(unique = True)
    invitation_status = models.ForeignKey(InvitationStatus,on_delete = models.SET_NULL,null=True)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    name = models.CharField(max_length = 10)
    profile_pic = models.FileField(upload_to='profile/')
    city = models.CharField(max_length = 200)
    contact_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    guests = models.ManyToManyField(Guest)



# Create your models here.
