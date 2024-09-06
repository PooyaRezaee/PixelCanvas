import re
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from core import simple_send_mail, logger


class UserManager(BaseUserManager):
    def create_user(self, username: str, password: str, **extra_fields):
        if not username:
            raise ValueError("You should enter username")

        if not password:
            raise ValueError("You should enter Password")
        
        # if 'email' in extra_fields.keys(): # For set optional email
        # extra_fields['email'] = self.normalize_email(extra_fields['email'])
        user = self.model(username=username, **extra_fields)

        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username: str, password: str, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    # email = models.EmailField(_("email address"), unique=True) # NOTE for later as new feature
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        null=True,
        unique=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    joined_at = models.DateTimeField(_("date joined"), auto_now_add=True)

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def send_email(self, subject: str, msg: str) -> bool:
        try:
            simple_send_mail(subject, msg, self.email)
            return True
        except Exception as e:
            logger.warning(f"can't send email for {self.pk}-{self.email} because {e}")
            return False
    
    @property
    def is_staff(self):
        return self.is_admin