import os

from todolist.settings import TELEGRAM_BOT_TOKEN
from .client import TgClient
from .dc import get_updates_schema, send_message_schema

tg_client = TgClient(TELEGRAM_BOT_TOKEN)

__all__ = ("get_updates_schema", "send_message_schema", "tg_client", "TgClient")
