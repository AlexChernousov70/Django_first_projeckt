from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """Кастомная модель пользователя с дополнительными полями"""
    first_name = None
    last_name = None

    # Делаем email уникальным и обязательным для логина
    email = models.EmailField(unique=True) 

    avatar = models.ImageField(
        upload_to='users/avatars/',
        blank=True,
        null=True,
        verbose_name=_('Аватар')
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Дата рождения')
    )
    telegram_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('Telegram ID')
    )
    github_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('GitHub ID')
    )

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return self.username