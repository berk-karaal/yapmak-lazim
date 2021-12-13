from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("Users must have an email address.")
        if not name:
            raise ValueError("Users must have a name.")
        if not password:
            raise ValueError("Users must have a password.")

        user = self.model(
            # email=self.normalize_email(email), # This is the suggested way, but this project uses all lowercase emails for authentication (which is wrong but easier ;) )
            email=email.lower(),
            name=name,
        )
        user.set_password(password)  # convert and update user.password to hashed format
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(email=email, name=name, password=password)
        user.is_admin = True
        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser):
    # identifier field (needs to be unique=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"  # set as identifier

    name = models.CharField(max_length=100)  # This is a custom field for our model
    register_date = models.DateTimeField(auto_now_add=True)

    EMAIL_FIELD = "email"  # return "email" for get_email_field_name()

    REQUIRED_FIELDS = [
        "name",
    ]  # these fields will be asked after createsuperuser command (USERNAME FIELD and passwords already included)

    is_active = models.BooleanField(default=True)  # default value = True
    is_admin = models.BooleanField(default=False)  # not built-in

    @property
    def is_staff(self):
        # Simplest possible answer: All admins are staff
        return self.is_admin

    # attach an user manager
    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
