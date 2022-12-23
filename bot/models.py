from django.core.validators import MinLengthValidator
from django.db import models


class TgUser(models.Model):
    tg_chat_id = models.BigIntegerField()
    tg_user_id = models.BigIntegerField(unique=True)
    tg_username = models.CharField(max_length=32, validators=[MinLengthValidator(5)], null=True)
    user = models.ForeignKey('core.User', null=True, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=32, unique=True)

# from django.db import models
# from django.core.validators import MinLengthValidator
# from django.utils.crypto import get_random_string
#
#
# class TgUser(models.Model):
#     class Meta:
#         verbose_name = "Пользователь Telegram"
#         verbose_name_plural = "Пользователи Telegram"
#
#     tg_chat_id = models.BigIntegerField(verbose_name="id чата")
#     tg_user_id = models.BigIntegerField(unique=True, verbose_name="id пользователя")
#     tg_username = models.CharField(
#         max_length=32,
#         validators=[MinLengthValidator(5)],
#         null=True, blank=True,
#         verbose_name="Имя пользователя"
#     )
#     user = models.ForeignKey(
#         "core.User",
#         null=True,
#         blank=True,
#         on_delete=models.CASCADE,
#         verbose_name="Пользователь приложения"
#     )
#     verification_code = models.CharField(max_length=15, unique=True, verbose_name="Код верификации")
#
#     def generate_verification_code(self) -> str:
#         code = get_random_string(15)
#         self.verification_code = code
#         self.save()
#         return code
