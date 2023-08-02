from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from habit.models import Habit
from users.models import User, UserRoles


class HabitsTestCase(APITestCase):
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
        self.test_model_name = 'habit_for_test'

    def test_habit_create(self):
        """Тест создания модели Habit"""
        habit_test = Habit.objects.create(name=self.test_model_name, place="home", time="17:53",
                                          action="pump up the press test",
                                          is_pleasurable=True, periodic=1, reward=None, execution_time="00:02",
                                          public=True, owner=self.user, associated_habit=None)
        response = self.client.post('/api/habits/', {'name': self.test_model_name, "place": "home", "time": "17:53",
                                                     "action": "pump up the press test", "is_pleasurable": True,
                                                     "periodic": 1, "reward": 'None', "execution_time": "00:02",
                                                     "public": True, "owner": 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(habit_test.name, 'habit_for_test')

    def test_get_habit(self):
        """Тест деталей модели Habit"""
        self.test_habit_create()
        response = self.client.get(f'/api/habits/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'id': 1, 'name': 'habit_for_test', 'place': 'home', 'time': '17:53:00',
                                           'action': 'pump up the press test', 'is_pleasurable': True, 'periodic': 1,
                                           'reward': None, 'execution_time': '00:02:00', 'public': True, 'owner': 1,
                                           'associated_habit': None})

    def test_list_habits(self):
        """Тест списка модели Habit"""
        self.test_habit_create()
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.json(), {'count': 2, 'next': None, 'previous': None, 'results': [{'id': 1, 'name': 'habit_for_test', 'place': 'home', 'time': '17:53:00', 'action': 'pump up the press test', 'is_pleasurable': True, 'periodic': 1, 'reward': None, 'execution_time': '00:02:00', 'public': True, 'owner': 1, 'associated_habit': None}, {'id': 2, 'name': 'habit_for_test', 'place': 'home', 'time': '17:53:00', 'action': 'pump up the press test', 'is_pleasurable': True, 'periodic': 1, 'reward': 'None', 'execution_time': '00:02:00', 'public': True, 'owner': 1, 'associated_habit': None}]})
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_list_habits_public(self):
        """Тест списка модели Habit публичности"""
        self.test_habit_create()
        response = self.client.get('/api/public_habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.json(), {'count': 2, 'next': None, 'previous': None, 'results': [{'id': 1, 'name': 'habit_for_test', 'place': 'home', 'time': '17:53:00', 'action': 'pump up the press test', 'is_pleasurable': True, 'periodic': 1, 'reward': None, 'execution_time': '00:02:00', 'public': True, 'owner': 1, 'associated_habit': None}, {'id': 2, 'name': 'habit_for_test', 'place': 'home', 'time': '17:53:00', 'action': 'pump up the press test', 'is_pleasurable': True, 'periodic': 1, 'reward': 'None', 'execution_time': '00:02:00', 'public': True, 'owner': 1, 'associated_habit': None}]})
        self.assertEqual(Habit.objects.all().count(), 2)
