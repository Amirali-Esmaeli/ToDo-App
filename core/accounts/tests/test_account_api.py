from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from accounts.models import User


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = User.objects.create_user(
        email="Test@Test.com", password="Amirali83!", is_verified=True
    )
    return user


@pytest.fixture
def unverified_user():
    user = User.objects.create_user(
        email="notverified@example.com",
        password="Test1234!",
        is_verified=False,
    )
    return user


@pytest.mark.django_db
class TestAccountApi:
    def test_post_registration_response_201_status(self, api_client):
        url = reverse("accounts:api-v1:registration")
        data = {
            "email": "tests@tests.com",
            "password": "Amirali83!",
            "password1": "Amirali83!",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == 201
        assert response.data["email"] == "tests@tests.com"

    def test_post_registration_invalid_data_response_400_status(
        self, api_client
    ):
        url = reverse("accounts:api-v1:registration")
        data = {
            "email": "invalid-email",
            "password": "Amirali83!",
            "password1": "123",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == 400

    def test_put_change_password_response_200_status(
        self, api_client, common_user
    ):
        url = reverse("accounts:api-v1:change-password")
        data = {
            "old_password": "Amirali83!",
            "new_password": "NewPass456!",
            "new_password1": "NewPass456!",
        }
        user = common_user
        api_client.force_login(user=user)
        response = api_client.put(url, data)
        assert response.status_code == 200

    def test_put_change_password_response_400_status(
        self, api_client, common_user
    ):
        url = reverse("accounts:api-v1:change-password")
        data = {
            "old_password": "Amirali83!",
            "new_password": "NewPass456!",
            "new_password1": "NewPass777!",
        }
        user = common_user
        api_client.force_login(user=user)
        response = api_client.put(url, data)
        assert response.status_code == 400

    def test_unverified_user_cannot_login(self, api_client, unverified_user):
        url = reverse("accounts:api-v1:token-login")
        data = {"email": "notverified@example.com", "password": "Test1234!"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == 400

    def test_verified_user_can_login(self, api_client, common_user):
        url = reverse("accounts:api-v1:token-login")
        data = {"email": "Test@Test.com", "password": "Amirali83!"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == 200
