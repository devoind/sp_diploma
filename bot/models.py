from django.db import models

import string
import random

from core.models import User


class TgUser(models.Model):
    tg_chat_id = models.BigIntegerField(verbose_name='TG CHAT_ID')
    tg_user_id = models.BigIntegerField(unique=True, verbose_name='TG USER_ID')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, default=None)
    verification_code = models.CharField(max_length=10, unique=True)
    username = models.CharField(
        max_length=255,
        verbose_name='TG USERNAME',
        null=True,
        blank=True,
        default=None
    )

    def set_verification_code(self):
        code = string.digits + string.ascii_letters
        verification_code = ''

        for _ in range(6):
            verification_code += code[random.randrange(0, len(code))]

        self.verification_code = verification_code
        self.save()

    class Meta:
        verbose_name = 'TG пользователь'
        verbose_name_plural = 'TG пользователи'
