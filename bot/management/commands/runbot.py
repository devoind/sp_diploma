from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from bot.utils_for_bot import BotGoal
from todolist import settings


class Command(BaseCommand):

    def __init__(self, *args: str, **kwargs: int):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.TELEGRAM_BOT_TOKEN)

    def verified_user(self, tg_user: TgUser, msg: Message):
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

    def add_user(self, msg: Message):
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

    def handle(self, *args: str, **kwargs: int):
        offset = 0

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.add_user(item.message)
