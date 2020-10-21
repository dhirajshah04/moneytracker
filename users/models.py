from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from model_utils import Choices

from .validators import UsernameValidator

USER_ROLES = Choices(
    'superadmin',
    'enduser',
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Please enter a valid Email Address")

        if not kwargs.get('username'):
            raise ValueError('Please enter a valid username')

        user = self.model(
            username=kwargs.get('username').strip(),
            email=self.normalize_email(email),
            first_name=kwargs.get('first_name'),
            middle_name=kwargs.get('middle_name'),
            last_name=kwargs.get('last_name'),
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)

        user.role = 'superadmin'
        user.is_confirmed = True
        user.save()

        return user


class User(AbstractBaseUser):
    username = models.CharField(
        max_length=250,
        unique=True,
        validators=[UsernameValidator()],
        error_messages={
            'unique': 'username already taken',
        },
    )

    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'email already exist',
        },
    )
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255)
    is_confirmed = models.BooleanField(default=False)
    role = models.CharField(max_length=100, choices=USER_ROLES, default=USER_ROLES.superadmin)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    object = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'user_user'

    def get_full_name(self):
        full_name = self.first_name

        if self.middle_name:
            full_name = full_name + ' ' + self.middle_name

        if self.last_name:
            full_name = full_name + ' ' + self.last_name

        return full_name

    def get_short_name(self):
        return self.first_name

    def is_superadmin(self):
        return self.role == USER_ROLES.superadmin

    def is_enduser(self):
        return self.role == USER_ROLES.enduser
