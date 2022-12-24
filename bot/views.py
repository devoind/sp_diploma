from rest_framework import generics, status
from rest_framework.response import Response
# from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from bot.models import TgUser
from bot.serializers import TgUserSerializer
from bot.tg.client import TgClient
from todolist.settings import TELEGRAM_BOT_TOKEN


class BotVerifyView(generics.UpdateAPIView):
    model = TgUser
    serializer_class = TgUserSerializer
    http_method_names = ['patch']
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        data = self.serializer_class(request.data).data
        tg_client = TgClient(token=TELEGRAM_BOT_TOKEN)
        tg_user = TgUser.objects.filter(verification_code=data['verification_code']).first()

        if not tg_user:
            Response(status=status.HTTP_400_BAD_REQUEST)
            # raise Exception
        # self.serializer_class.update(instance=tg_user, data=data)
        tg_user.user = request.user
        tg_user.save()
        tg_client.send_message(chat_id=tg_user.tg_chat_id, text='Успешно!')
        return Response(data=data, status=status.HTTP_201_CREATED)

    # def get_object(self):
    #     return get_object_or_404(TgUser, verification_code=self.request.data['verification_code'])

