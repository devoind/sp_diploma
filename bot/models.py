from django.db import models

import string
import random


class TgUser(models.Model):
    tg_chat_id = models.BigIntegerField(verbose_name='TG CHAT_ID')
    tg_user_id = models.BigIntegerField(unique=True, verbose_name='TG USER_ID')
    user = models.ForeignKey('core.User', null=True, blank=True, verbose_name='Пользователь',
                             on_delete=models.PROTECT)
    verification_code = models.CharField(max_length=6, unique=True)
    username = models.CharField(
        max_length=255,
        verbose_name='TG USERNAME',
        null=True,
        blank=True
    )

    def set_verification_code(self):
        length = 10  # Длина кода подтверждения
        digits = string.digits
        v_code = ''.join(random.sample(digits, length))
        self.verification_code = v_code

    class Meta:
        verbose_name = 'Telegram пользователь'
        verbose_name_plural = 'Telegram пользователи'
