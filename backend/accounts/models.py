import uuid

from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username,email, password=None, license_type='DEMO', **extra_fields):
        """
        Create and return a regular user with an email, username, password, and dynamic inputs.
        """
        if not username:
            raise ValueError('The Username field must be set')

        # Create the user instance with the provided fields
        user = self.model(username=username,email=email, license_type=license_type, **extra_fields)

        # Set the user's password
        user.set_password(password)

        # Set allowable inputs based on license type
        user.set_allowable_inputs(license_type)
        user.set_fullname()

        # Save the user to the database
        user.save(using=self._db)
        return user

    def create_superuser(self, username,email, password=None, **extra_fields):
        """
        Create and return a superuser with email, username, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username=username, email=email, password=password, **extra_fields)


class LicenseChoices(models.TextChoices):
    DEMO = 'DEMO', 'Demo'
    FUTURE = 'FUTURE', 'Future'
    FULL = 'FULL', 'Full'


class CustomUser(AbstractBaseUser,PermissionsMixin):
    # id = models.BigAutoField(primary_key=True)  # Default primary key
    id=models.UUIDField(default=uuid.uuid4,editable=False,unique=True,primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    full_name = models.CharField(max_length=150, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    api_keys=models.JSONField(default=dict)



    @classmethod
    def set_fullname(cls):
        return f'{cls.first_name} {cls.last_name}'


    license_type = models.CharField(
        max_length=10,
        choices=LicenseChoices.choices,
        default=LicenseChoices.DEMO,
    )

    # Fields to store the allowable input values
    allowableLineInput = models.IntegerField(verbose_name="Allowable line input", default=200)
    allowableSizeInput = models.IntegerField(verbose_name="Allowable size input", default=5)

    @classmethod
    def set_allowable_inputs(cls, license_type):
        """
        Set the allowable line input and size input based on the license type.
        """
        if license_type == LicenseChoices.DEMO:
            return {"allowableLineInput": 200, "allowableSizeInput": 5}
        elif license_type == LicenseChoices.FUTURE:
            return {"allowableLineInput": 500, "allowableSizeInput": 10}
        elif license_type == LicenseChoices.FULL:
            return {"allowableLineInput": 1000, "allowableSizeInput": 50}
        return {"allowableLineInput": 0, "allowableSizeInput": 0}

    def update_limits_from_license(self):
        """
        Update the allowable inputs based on the current user's license type.
        """
        limits = self.set_allowable_inputs(self.license_type)
        self.allowableLineInput = limits['allowableLineInput']
        self.allowableSizeInput = limits['allowableSizeInput']
        self.save()
    objects=CustomUserManager()
    class Meta:
        pass
    USERNAME_FIELD = 'username' # Used for authentication
    REQUIRED_FIELDS = ['email'] # Required for creating superuser

    def __str__(self):
        return self.username

#TODO add user profile model
#todo add user update signal
