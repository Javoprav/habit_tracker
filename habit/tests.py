from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User, UserRoles


class  CourseTestCase(APITestCase):
    """Тесты модели Habit"""
    def setUp(self) -> None:
        """Подготовка данных перед каждым тестом"""
        self.user = User.objects.create(
            email='user@user.com',
            is_staff=False,
            is_superuser=False,
            is_active=True,
            role=UserRoles.MEMBER,
            chat_id=378037756
        )
        self.user.set_password('123')
        self.user.save()
        response = self.client.post('/api/token/', {"email": "user@user.com", "password": "123"})
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.test_model_name = 'course_for_test'
