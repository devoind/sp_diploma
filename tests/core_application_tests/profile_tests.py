import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import User
from core.serializers import ProfileSerializer


@pytest.mark.django_db
def test_profile(auth_client: APIClient, test_user: User) -> None:
    response = auth_client.get(reverse('user_profile'))
    expected_response = ProfileSerializer(instance=test_user).data

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_response


@pytest.mark.django_db
def test_update_password(auth_client: APIClient, test_user: User) -> None:
    response = auth_client.put(
        reverse('user_update_password'),
        data={
            'new_password': '666Weid777',
            'old_password': '007PassW123',
        },
    )

    assert response.status_code == status.HTTP_200_OK
