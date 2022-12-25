from typing import Optional, List

from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from bot.tg.client import TgClient
from bot.models import TgUser
from bot.tg.dc import GetUpdatesResponse, Message
from goals.models import Goal, GoalCategory
import datetime

from todolist.settings import TELEGRAM_BOT_TOKEN


class Command(BaseCommand):
    help: str = 'Command to start TodolistBot'
    offset: int = 0

    def handle(self, *args, **options):
        tg_client = TgClient(token=TELEGRAM_BOT_TOKEN)

        while True:
            response: GetUpdatesResponse = tg_client.get_updates(offset=self.offset)
            for item in response.result:
                self.offset = item.update_id + 1
                if not item.message:
                    continue
                # state A пользователя нет в базе данных
                tg_user: TgUser = self.get_tg_user(item.message)
                if not tg_user:
                    verification_code: str = self.generate_verification_code()
                    self.create_tg_user(item.message, tg_client, verification_code)
                    continue

                # state B пользователь есть в базе, но не подтвержден
                if tg_user.user_id is None:
                    verification_code: str = self.generate_verification_code()
                    self.update_tg_user_verification_code(item.message, tg_client, verification_code)
                    continue

                # state C пользователь есть в базе и подтвержден
                if item.message.text.strip().lower() == '/goals':
                    self.get_goals(item.message, tg_user, tg_client)
                elif item.message.text.strip().lower() == '/create':  # state Create 1
                    goal_categories: list = self.get_goal_categories(item.message, tg_user, tg_client)
                    goal_category = self.choose_goal_category(tg_client, goal_categories)
                    if goal_category:
                        tg_client.send_message(
                            chat_id=item.message.chat.id,
                            text=f'Вы выбрали категорию:  {goal_category.title}\n Введите название цели\n'
                                 f'(Чтобы прервать операцию, введите команду /cancel)')
                        self.create_goal(tg_client, tg_user, goal_category)
                else:
                    tg_client.send_message(
                        chat_id=item.message.chat.id,
                        text='Неизвестная команда\n\nДоступны команды:\n'
                             ' /goals - просмотреть цели\n/create - создать цель')
                    continue

    def get_tg_user(self, message: Message):
        try:
            tg_user: Optional[TgUser] = TgUser.objects.get(tg_user_id=message.msg_from.id)
        except:
            return None

        return tg_user

    def generate_verification_code(self) -> str:
        return get_random_string(length=32)

    def create_tg_user(self, message: Message, tg_client: TgClient, verification_code: str) -> None:
        TgUser.objects.create(
            tg_chat_id=message.chat.id,
            tg_user_id=message.msg_from.id,
            tg_username=message.msg_from.username,
            verification_code=verification_code
        )
        tg_client.send_message(chat_id=message.chat.id,
                               text=f'Привет, {message.msg_from.first_name}!\n'
                                    f'[verification_code]: {verification_code}')

    def update_tg_user_verification_code(self, message, tg_client, verification_code) -> None:
        tg_user: Optional[TgUser] = TgUser.objects.filter(tg_user_id=message.msg_from.id)
        if tg_user:
            tg_user.objects.update(
                verification_code=verification_code
            )
            tg_client.send_message(chat_id=message.chat.id,
                                   text=f'Привет, {message.msg_from.first_name}!\n'
                                        f'[Verification_code]: {verification_code}')

    def get_goals(self, message: Message, tg_user: TgUser, tg_client: TgClient) -> None:
        goals: Optional[List[Goal]] = Goal.objects.filter(
            category__board__participants__user__id=tg_user.user_id).exclude(status=Goal.Status.archived)
        if goals:
            goals_str: str = f'Ваши цели:'
            for goal in goals:
                goals_str += f'\n\n{goal.title}\nприоритет: ' \
                             f'{goal.Priority.choices[goal.priority-1][1]}\nсрок: {goal.due_date}'
        else:
            goals_str: str = f'У Вас нет целей'

        tg_client.send_message(chat_id=message.chat.id, text=goals_str)

    def get_goal_categories(self, message: Message, tg_user: TgUser, tg_client: TgClient) -> Optional[List[GoalCategory]]:
        goal_categories: Optional[List[GoalCategory]] = GoalCategory.objects.filter(
            board__participants__user__id=tg_user.user_id, is_deleted=False)
        if goal_categories:
            list_goal_categories: list = [goal_category.title for goal_category in goal_categories]
            goal_categories_str: str = f'Введите одну из категорий:\n' \
                                       f'(Чтобы прервать операцию, введите команду /cancel) \n\n' \
                                       f'' + '\n'.join(list_goal_categories)
        else:
            goal_categories_str: str = f'У Вас нет ни одной категории'
        tg_client.send_message(chat_id=message.chat.id, text=goal_categories_str)

        return goal_categories

    def choose_goal_category(self, tg_client: TgClient, goal_categories: List[GoalCategory]) -> Optional[GoalCategory]:
        while True:
            response: GetUpdatesResponse = tg_client.get_updates(offset=self.offset)
            for item in response.result:
                self.offset = item.update_id + 1
                if not item.message:
                    continue

                if item.message.text.strip().lower() == '/cancel':
                    tg_client.send_message(chat_id=item.message.chat.id, text='Cоздание цели прервано')
                    return None

                elif item.message.text.strip().lower() in [goal_category.title for goal_category in goal_categories]:
                    for goal_category in goal_categories:
                        if item.message.text.strip().lower() == goal_category.title:
                            return goal_category
                else:
                    tg_client.send_message(
                        chat_id=item.message.chat.id,
                        text='Такой категории нет, повторите ввод\n (Чтобы прервать операцию, введите команду /cancel)')

    def create_goal(self, tg_client: TgClient, tg_user: TgUser, goal_category: GoalCategory) -> None:
        while True:
            response: GetUpdatesResponse = tg_client.get_updates(offset=self.offset)
            for item in response.result:
                self.offset = item.update_id + 1
                if not item.message:
                    continue

                if item.message.text.strip().lower() == '/cancel':
                    tg_client.send_message(chat_id=item.message.chat.id, text='Cоздание цели прервано')
                    return
                else:
                    due_date = datetime.date.today() + datetime.timedelta(days=14)
                    goal = Goal.objects.create(
                        category=goal_category,
                        user=tg_user.user,
                        title=item.message.text,
                        description='Цель создана в Telegram',
                        due_date=due_date.strftime('%Y-%m-%d')
                    )
                    tg_client.send_message(
                        chat_id=item.message.chat.id, text=f'Цель [{goal.title}] успешно создана')
                    return
