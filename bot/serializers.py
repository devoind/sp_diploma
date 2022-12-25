from rest_framework import serializers

from bot.models import TgUser
from bot.tg.client import TgClient
from todolist.settings import TELEGRAM_BOT_TOKEN


class TgUserSerializer(serializers.ModelSerializer):
    user_id = serializers.CurrentUserDefault
    tg_id = serializers.IntegerField(source='tg_user_id')
    username = serializers.CharField(source='tg_username')

    class Meta:
        model = TgUser
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.user = self.context['request'].user
        instance.save()
        TgClient(token=TELEGRAM_BOT_TOKEN).send_message(chat_id=instance.tg_chat_id,
                                                        text='Верификация прошла успешно')
        return instance
