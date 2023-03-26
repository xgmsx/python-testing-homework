from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User

if TYPE_CHECKING:
    from tests.plugins.identity.user import (
        RegistrationData,
        RegistrationDataFactory,
        UserAssertion,
        UserData,
    )

REQUIRED_FIELD_WITHOUT_BIRTHDAY = list(
    set(User.REQUIRED_FIELDS) - {User.BIRTHDAY_FIELD},
)


@pytest.mark.django_db()
def test_registration_page_renders(client: Client) -> None:
    """Basic `get` method works."""
    response = client.get(reverse('identity:registration'))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_valid_registration(
    client: Client,
    registration_data: 'RegistrationData',
    user_data: 'UserData',
    assert_correct_user: 'UserAssertion',
) -> None:
    """Test that registration works with correct data."""
    response = client.post(
        reverse('identity:registration'),
        data=registration_data,
    )
    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('identity:login')
    assert_correct_user(registration_data['email'], user_data)


@pytest.mark.django_db()
@pytest.mark.parametrize(
    'field', REQUIRED_FIELD_WITHOUT_BIRTHDAY + [User.USERNAME_FIELD],
)
def test_registration_missing_required_field(
    client: Client,
    registration_data_factory: 'RegistrationDataFactory',
    field: str,
) -> None:
    """Test that missing required will fail the registration."""
    post_data = registration_data_factory(
        **{field: ''},  # type: ignore[arg-type]
    )
    response = client.post(
        reverse('identity:registration'),
        data=post_data,
    )
    assert response.status_code == HTTPStatus.OK
    assert not User.objects.filter(email=post_data['email'])


@pytest.mark.django_db()
@pytest.mark.parametrize(
    'field', REQUIRED_FIELD_WITHOUT_BIRTHDAY + [User.USERNAME_FIELD],
)
def test_registration_forgotten_required_field(
    client: Client,
    registration_data_factory: 'RegistrationDataFactory',
    field: str,
) -> None:
    """Test that missing required will fail the registration."""
    post_data = registration_data_factory()
    post_data.pop(field)  # type: ignore[misc]
    response = client.post(
        reverse('identity:registration'),
        data=post_data,
    )
    assert response.status_code == HTTPStatus.OK
    if field != 'email':
        assert not User.objects.filter(email=post_data['email'])
