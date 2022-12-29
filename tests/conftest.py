import pytest
import factories

from pytest_factoryboy import register
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()

register(factory_class=factories.UserFactory, _name='user')
register(factory_class=factories.BoardFactory, _name='board')
register(factory_class=factories.GoalCategoryFactory, _name='category')
register(factory_class=factories.BoardParticipant, _name='board_participant')


@pytest.fixture
def auth_client(test_user):
    client = APIClient()
    client.login(username='Weid', password='007Weid007')
    return client


# @pytest.fixture
# def test_user(db):
#     user = USER_MODEL.objects.create(
#         username='Weid',
#         password='007Weid007',
#         email='test@tr.ru',
#     )
#     return user
