from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    email = models.EmailField(
        unique=True,
        help_text='Email',
        error_messages={
            'unique': 'Пользователь с такой почтой уже существует.',
            'invalid': 'Почта недействительна',
        }
    )

    def __str__(self):
        return self.username
