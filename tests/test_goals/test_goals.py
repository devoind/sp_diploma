import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_create_goal(auth_client, test_user, category):
    url = reverse('create_goal')
    response = auth_client.post(
        path=url,
        data={
            'title': 'New Goal',
            'category': category.pk,
        }
    )

    assert response.status_code == '201'
