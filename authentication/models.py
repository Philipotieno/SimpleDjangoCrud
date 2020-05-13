from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin, Group)
from django.db import models
from .choices import (SERVICE_CHOICES, UNIT_CHOICES, RANK_CHOICES)
import jwt


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free.

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, *args, **kwargs):
        """Create and return a `User` with a surname, reg_number and password."""
        password = kwargs.get('password', '')
        reg_number = kwargs.get('reg_number', '')
        del kwargs['reg_number']
        del kwargs['password']
        user = self.model(reg_number=reg_number, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, *args, **kwargs):
        """
        Create and return a `User` with superuser powers.
        Superuser powers means that this user is an admin that can do anything
        they want.
        """
        password = kwargs.get('password', '')
        reg_number = kwargs.get('reg_number', '')
        del kwargs['reg_number']
        del kwargs['password']
        user = self.model(reg_number=reg_number, **kwargs)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.
    first_name = models.CharField(db_index=True, max_length=255, unique=False)

    last_name = models.CharField(db_index=True, max_length=255, unique=False)

    surname = models.CharField(db_index=True, max_length=255, unique=False)

    reg_number = models.CharField(db_index=True, max_length=15, unique=True)

    is_active = models.BooleanField(default=True)

    groups = models.ForeignKey(Group, on_delete=models.CASCADE)

    # The `is_staff` flag is expected by Django to determine who can and cannot
    # log into the Django admin site. For most users, this flag will always be
    # falsed.
    is_staff = models.BooleanField(default=False)
    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case, we want that to be the reg_number field.
    USERNAME_FIELD = 'reg_number'
    REQUIRED_FIELDS = ['groups_id', 'surname', 'first_name',
                       'last_name']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()


    def __str__(self):
        """
            Returns a string representation of this `User`.
            This string is used when a `User` is printed in the console.
        """
        return self.surname


    def token(self):
        """
            This method allows us to get the jwt token by calling the user.token
            method.
        """
        return self.generate_jwt_token()

    def generate_jwt_token(self):
        """
            This method allows the creation of a jwt token. User's surname and
            reg_number are used in the encoding of the token.
            The token is generated during sign up.
        """
        user_details = {'reg_number': self.reg_number,
                        'surname': self.surname}
        token = jwt.encode(
            {
                'user_data': user_details,
                'exp': datetime.now() + timedelta(hours=24)
            }, settings.SECRET_KEY, algorithm='HS256'
        )
        return token.decode('utf-8')