from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message

from bot.utils_for_bot import BotGoal
from todolist import settings


class Command(BaseCommand):
    help = 'Run Telegram Bot'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.TELEGRAM_BOT_TOKEN)

    def verified_user(self, tg_user: TgUser, msg: Message) -> None:
        if msg.text == '/goals':
            BotGoal(tg_user=tg_user, msg=msg, tg_client=self.tg_client).get_goal()
        elif msg.text == '/start':
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text=f'Вы уже подтвердили свою личность!✅'
            )
        elif 'create' in msg.text:
            BotGoal(tg_user=tg_user, msg=msg, tg_client=self.tg_client).create_goal()
        elif msg.text == '/cancel':
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text=f'Операция отменена!✅'
            )
        else:
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text=f'Неизвестная команда!🤔'
            )

    def add_user(self, msg: Message) -> None:
        tg_user, create = TgUser.objects.get_or_create(
            tg_user_id=msg.from_.id,
            tg_chat_id=msg.chat.id,
            username=msg.from_.username
        )
        if create:
            self.tg_client.send_message(chat_id=msg.chat.id, text='Зарегистрировал вас!👌')
        if tg_user.user:
            self.verified_user(tg_user=tg_user, msg=msg)
        else:
            BotGoal(tg_user=tg_user, msg=msg, tg_client=self.tg_client).check_user()

    def handle(self, *args: str, **kwargs: int) -> None:
        offset = 0

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.add_user(item.message)

    # def handle(self, *args, **kwargs):
    #     offset = 0
    #
    #     while True:
    #         response = self.tg_client.get_updates(offset=offset)
    #         for item in response.result:
    #             offset = item.update_id + 1
    #             tg_user, created = TgUser.objects.get_or_create(tg_chat_id=item.message.chat.id,
    #                                                             tg_user_id=item.message.from_.id)
    #
    #             if created:
    #                 tg_user.set_verification_code()
    #                 self.tg_client.send_message(tg_user.tg_chat_id,
    #                                             f'Привет. Подтверди, пожалуйста, свой аккаунт. '
    #                                             f'Для подтверждения необходимо ввести код: '
    #                                             f'{tg_user.verification_code}')
    #                 continue
    #
    #             elif not tg_user.user:
    #                 tg_user.set_verification_code()
    #                 self.tg_client.send_message(tg_user.tg_chat_id,
    #                                             f'Для дальнейшей работы подтвердите, пожалуйста, свой аккаунт. '
    #                                             f'Для подтверждения необходимо ввести код: '
    #                                             f'{tg_user.verification_code}')
    #                 continue
    #
    #             if item.message.text == '/goals':
    #                 user = tg_user.user
    #                 goals = Goal.objects.filter(category__board__participants__user=user)
    #
    #                 for goal in goals:
    #                     self.tg_client.send_message(tg_user.tg_chat_id,
    #                                                 f'Название {goal.title}, \n '
    #                                                 f'Категория {goal.category}, \n'
    #                                                 f'Статус {goal.get_status_display()}, \n'
    #                                                 f'Дедлайн {goal.due_date if goal.due_date else "Нет"} \n')
    #
    #             else:
    #                 self.tg_client.send_message(tg_user.tg_chat_id, 'Неизвестная команда')
