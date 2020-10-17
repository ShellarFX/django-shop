import re

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core import validators
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager


class UsernameValidator(validators.RegexValidator):
    regex = r'^[\w]+\Z'
    message = 'Введите правильное имя пользователя. Оно может содержать только лат. символы и цифры'
    flags = re.ASCII


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username_validator = UsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=32,
        unique=True,
        help_text='Не больше 32 символов. Только лат. символы и цифры',
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), blank=True)
    balance = models.IntegerField(
        'Баланс',
        default=0,
    )
    is_seller = models.BooleanField(
        'Продавец',
        default=False,
        help_text='Является ли пользователь продавцом'
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    created_at = models.DateTimeField(_('date joined'), default=timezone.now)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'