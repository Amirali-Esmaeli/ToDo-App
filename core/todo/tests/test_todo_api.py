from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from accounts.models import User
from ..models import Task


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


@pytest.fixture
def user_task(common_user):
    return Task.objects.create(title="My task", user=common_user)


@pytest.fixture
def another_verified_user(db):
    return User.objects.create_user(
        email="another@example.com", password="Test1234!", is_verified=True
    )


@pytest.mark.django_db
class TestTodoApi:

    def test_get_todo_response_200_status(self, api_client, common_user):
        url = reverse("todo:api-v1:task-list")
        user = common_user
        api_client.force_login(user=user)
        response = api_client.get(url)
        assert response.status_code == 200

    def test_get_todo_response_401_status(self, api_client):
        url = reverse("todo:api-v1:task-list")
        response = api_client.get(url)
        assert response.status_code == 401

    def test_create_todo_response_201_status(self, api_client, common_user):
        url = reverse("todo:api-v1:task-list")
        data = {
            "title": "test",
        }
        user = common_user
        api_client.force_login(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert response.data["title"] == data["title"]

    def test_create_todo_response_401_status(self, api_client):
        url = reverse("todo:api-v1:task-list")
        data = {
            "title": "test",
        }
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_create_todo_invalid_data_response_400_status(
        self, api_client, common_user
    ):
        url = reverse("todo:api-v1:task-list")
        data = {}
        user = common_user
        api_client.force_login(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_unverified_user_cannot_create_task(
        self, api_client, unverified_user
    ):
        api_client.force_login(user=unverified_user)
        url = reverse("todo:api-v1:task-list")
        data = {
            "title": "New Task",
        }
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_verified_user_can_edit_own_task(
        self, api_client, common_user, user_task
    ):
        api_client.force_login(user=common_user)
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": user_task.pk})
        data = {"title": "Updated Task"}
        response = api_client.patch(url, data)
        assert response.status_code == 200
        assert response.data["title"] == data["title"]

    def test_verified_user_cannot_edit_others_task(
        self, api_client, another_verified_user, user_task
    ):
        api_client.force_login(user=another_verified_user)
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": user_task.pk})
        data = {"title": "Hacked Task"}
        response = api_client.patch(url, data)
        assert response.status_code == 404

    def test_verified_user_can_delete_own_task(
        self, api_client, common_user, user_task
    ):
        api_client.force_login(user=common_user)
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": user_task.pk})
        response = api_client.delete(url)
        assert response.status_code == 204

    def test_verified_user_cannot_delete_others_task(
        self, api_client, another_verified_user, user_task
    ):
        api_client.force_login(user=another_verified_user)
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": user_task.pk})
        response = api_client.delete(url)
        assert response.status_code == 404
