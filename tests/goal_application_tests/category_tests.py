import pytest
from django.urls import reverse
from rest_framework import status

from goals.serializers import GoalCategorySerializer


@pytest.mark.django_db
def test_create_category(auth_client, test_user, board, board_participant):
    url = reverse('category_goal_create')
    payload = {
        'user': test_user.pk,
        'board': board.pk,
        'title': 'Новая категория',
        'is_deleted': True
    }

    response = auth_client.post(
        path=url,
        data=payload
    )
    response_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_data['board'] == payload['board']
    assert response_data['title'] == payload['title']
    assert response_data['is_deleted'] == payload['is_deleted']


@pytest.mark.django_db
def test_category_detail(auth_client, test_user, goal_category, board_participant):
    url = reverse('detail_update_delete_goal_category', kwargs={'pk': goal_category.id})
    response = auth_client.get(path=url)
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_data['user']['id'] == test_user.pk
    assert response_data['user']['username'] == test_user.username
    assert response_data['user']['email'] == test_user.email


@pytest.mark.django_db
def test_category_update(auth_client, test_user, goal_category, board_participant):
    url = reverse('detail_update_delete_goal_category', kwargs={'pk': goal_category.id})
    payload = {
        'title': 'Обновленная категория',
        'is_deleted': True
    }

    response = auth_client.patch(path=url, data=payload)
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_data['user']['id'] == test_user.pk
    assert response_data['user']['username'] == test_user.username
    assert response_data['user']['email'] == test_user.email


@pytest.mark.django_db
def test_category_delete(auth_client, goal_category, board_participant):
    url = reverse('detail_update_delete_goal_category', kwargs={'pk': goal_category.id})

    response = auth_client.delete(path=url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_category_list(auth_client, goal_category_list, board_participant):
    url = reverse('category_goal_list')

    response = auth_client.get(path=url)
    expected_response = GoalCategorySerializer(goal_category_list, many=True).data

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_response


@pytest.mark.django_db
def test_category_list_limit(auth_client, goal_category_list, board_participant):
    url = reverse('category_goal_list') + '?limit=10'

    response = auth_client.get(path=url)
    expected_response = GoalCategorySerializer(goal_category_list, many=True).data

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 10
    assert response.data['next'] is None
    assert response.data['previous'] is None
    assert response.data['results'] == expected_response
