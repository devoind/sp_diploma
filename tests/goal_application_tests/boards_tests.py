import json

import pytest
from django.urls import reverse
from rest_framework import status

from goals.serializers import BoardSerializers, BoardListSerializer
from goals.models import BoardParticipant


@pytest.mark.django_db
def test_board_create(auth_client):
    url = reverse('create_board')
    payload = {
        'title': 'Название доски',
        'is_deleted': True
    }
    response = auth_client.post(url, data=payload)
    response_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_data['title'] == payload['title']
    assert response_data['is_deleted'] == payload['is_deleted']


@pytest.mark.django_db
def test_board_detail(auth_client, test_user, board, board_participant):
    url = reverse('detail_update_delete_board', kwargs={'pk': board.id})
    response = auth_client.get(url)
    response_data = response.json()
    expected_data = BoardSerializers(board).data

    assert response.status_code == status.HTTP_200_OK
    assert response_data == expected_data


@pytest.mark.django_db
def test_board_update(auth_client, test_user, board, board_participant):
    url = reverse('detail_update_delete_board', kwargs={'pk': board.id})
    payload = {
        'participants': [],
        'title': 'Переименование доски'
    }
    response = auth_client.put(url, data=json.dumps(payload), content_type='application/json')
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_data['id'] == board.id
    assert response_data['participants'][0]['id'] == board_participant.pk
    assert response_data['participants'][0]['user'] == test_user.username


@pytest.mark.django_db
def test_board_delete(auth_client, test_user, board, board_participant):
    url = reverse('detail_update_delete_board', kwargs={'pk': board.id})
    response = auth_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_board_list(auth_client, test_user, board_list):
    board_participant = []
    for board_ in board_list:
        board_participant.append(BoardParticipant.objects.create(board=board_, user=test_user))
    url = reverse('list_board')
    expected_response = BoardListSerializer(board_list, many=True).data
    response = auth_client.get(url)
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_data == expected_response


@pytest.mark.django_db
def test_board_list_limit(auth_client, test_user, board_list):
    board_participant = []
    for board_ in board_list:
        board_participant.append(BoardParticipant.objects.create(board=board_, user=test_user))
    url = reverse('list_board') + '?limit=10'
    expected_response = BoardListSerializer(board_list, many=True).data
    response = auth_client.get(url)
    response_data = response.json()

    assert response_data['count'] == 10
    assert response_data['next'] is None
    assert response_data['previous'] is None
    assert response_data['results'] == expected_response
