from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, first_name, password, **other_fields):

        # Think of other_fiels as a dict whose default values are setting to True for superuser
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        # Calling the function below
        return self.create_user(email, username, first_name, password, **other_fields)

    def create_user(self, email, username, first_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email) # Gmail accepts multiple dots for e.g um.ar.sal.man1997@gmail.com would send to my gmail. 
        # So to avoid people making different accounts we do normalize
        user = self.model(email=email, username=username,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

# AbstractBaseUser allows you to override the django default user table
class NewUser(AbstractBaseUser, PermissionsMixin):

    # To change Table Name
    # class Meta:
    #     db_table = 'unique_users'

    # https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.Field.blank
    # https://docs.djangoproject.com/en/3.1/ref/models/fields/
    # Blank is for Validation and Null is for Database, by default both are False
    email = models.EmailField(_('email address'), unique=True) # _('email address') This syntax is to choose the name to set in Admin
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    
    # This is for Email Verification Services, if verify then change to True from False
    # https://pypi.org/project/django-email-verification/
    is_active = models.BooleanField(default=True)

    # customAccountManager to handle normal and super users
    objects = CustomAccountManager()

    # Email and username are both required to be unique
    USERNAME_FIELD = 'email'
    # Make these both required fields
    REQUIRED_FIELDS = ['username', 'first_name']

    def __str__(self):
        return self.username
