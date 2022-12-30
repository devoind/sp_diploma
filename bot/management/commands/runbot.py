from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import GoalCategory
from goals.models import Goal
from todolist.settings import TELEGRAM_BOT_TOKEN


class Command(BaseCommand):
    help = 'Run Telegram-Bot'

    def __init__(self, *args: str, **kwargs: int):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(TELEGRAM_BOT_TOKEN)
        self.offset = 0

    def handle(self, *args: str, **kwargs: int):

        while True:
            response = self.tg_client.get_updates(offset=self.offset)
            for item in response.result:
                self.offset = item.update_id + 1
                tg_user: TgUser | False = self.check_user(item.message)

                if not tg_user:
                    continue

                if item.message.text == '/goals':
                    self.get_goals(tg_user)
                elif item.message.text == '/create':
                    self.choice_category(tg_user)
                else:
                    self.tg_client.send_message(tg_user.tg_chat_id, 'Для просмотра списка задач введи /goals.\n'
                                                                    'Для создания задачи введи /create.\n'
                                                                    'Для отмены введи /cancel')

    def check_user(self, message: Message):
        """Проверка, есть ли пользователь в Telegram-Bot"""
        tg_user, created = TgUser.objects.get_or_create(tg_chat_id=message.chat.id, tg_user_id=message.from_.id)

        if created or not tg_user.user:
            tg_user.set_verification_code()
            self.tg_client.send_message(tg_user.tg_chat_id,
                                        f'Привет. Подтверди, пожалуйста, свой аккаунт. '
                                        f'Для подтверждения необходимо ввести код в приложении: '
                                        f'{tg_user.verification_code} на сайте skypro-evedrov.ga')
            return False
        return tg_user

    def get_goals(self, tg_user: TgUser):
        """Получение всех целей пользователя в Telegram-Bot"""
        goals = Goal.objects.filter(user=tg_user.user, status__in=[1, 2, 3])

        if goals.count() > 0:
            [self.tg_client.send_message(tg_user.tg_chat_id,
                                         f'Название {goal.title},\n'
                                         f'Категория {goal.category},\n'
                                         f'Статус {goal.get_status_display()},\n'
                                         f'Дедлайн {goal.due_date if goal.due_date else "Нет"} \n') for goal in goals]
        else:
            self.tg_client.send_message(tg_user.tg_chat_id, 'Нет задач')

    def choice_category(self, tg_user: TgUser):
        """Выбор категории для цели в Telegram-Bot"""
        categories = GoalCategory.objects.filter(board__participants__user=tg_user.user, is_deleted=False)
        self.tg_client.send_message(tg_user.tg_chat_id,
                                    f'Выбери категорию: {[category.title for category in categories]}\n'
                                    f'Для отмены введи /cancel')
        dict_categories = {item.title: item for item in categories}

        flag = True
        while flag:
            response = self.tg_client.get_updates(offset=self.offset)
            for item in response.result:
                self.offset = item.update_id + 1

                if item.message.text in dict_categories:
                    category = dict_categories.get(item.message.text)
                    self.create_goal(tg_user, category)
                    flag = False
                elif item.message.text == '/cancel':
                    flag = False
                else:
                    self.tg_client.send_message(tg_user.tg_chat_id, 'Категория не существует')

    def create_goal(self, tg_user: TgUser, category: GoalCategory):
        """Создание новой цели через Telegram-Bot"""
        self.tg_client.send_message(tg_user.tg_chat_id, 'Укажите название задачи. Для отмены введи /cancel')

        flag = True
        while flag:
            response = self.tg_client.get_updates(offset=self.offset)
            for item in response.result:
                self.offset = item.update_id + 1
                if item.message.text == '/cancel':
                    flag = False
                else:
                    goal = Goal(title=item.message.text, category=category, user=tg_user.user)
                    goal.save()

    # def create_goal(self, category: GoalCategory, tg_user: TgUser):
    #     """Создание новой цели через Telegram-Bot"""
    #     self.tg_client.send_message(chat_id=tg_user.chat_id, text=f'Введите заголовок цели')
    #
    #     flag = True
    #     while flag:
    #         response = self.tg_client.get_updates(offset=self.offset)
    #         for item in response.result:
    #             self.offset = item.update_id + 1
    #
    #             if item.message.text == '/cancel':
    #                 self.tg_client.send_message(chat_id=tg_user.chat_id, text='Операция отменена')
    #                 flag = False
    #
    #             else:
    #                 goal = Goal.objects.create(category=category, user=tg_user.user, title=item.message.text)
    #                 self.tg_client.send_message(
    #                     chat_id=tg_user.chat_id,
    #                     text=f'Цель создана\n'
    #                          f'{goal.title}\n'
    #                          f'{goal.category}'
    #                 )
    #                 flag = False
