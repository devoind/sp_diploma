import pytest
import factories

from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()


@pytest.fixture
def auth_client(test_user):
    client = APIClient()
    client.force_authenticate(test_user)
    return client


@pytest.fixture
def test_user(db):
    user = USER_MODEL.objects.create(
        username='Weid',
        password='007Weid007',
        email='test@tr.ru',
    )
    return user


@pytest.fixture
def category(board, test_user):
    return factories.GoalCategoryFactory.create(board=board, user=test_user)


@pytest.fixture
def board():
    return factories.BoardFactory.create()


@pytest.fixture
def board_participant(test_user, board):
    participant = factories.BoardParticipantFactory.create(
        board=board,
        user=test_user,
    )
    return participant
