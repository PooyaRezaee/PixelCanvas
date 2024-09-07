from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from model_bakery import baker
from ...services.user import create_user
from ...models import User


class UserServicesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = baker.make("account.User")
        cls.user2 = baker.make("account.User")

    def test_create_valid_user(self):
        username = "ausername"
        password = "NormalPassword123"
        user = create_user(username, password)

        self.assertIsInstance(user, User)
        self.assertEqual(user.username, username)
        self.assertNotEqual(user.password, password)

    def test_create_by_exist_username(self):
        username = self.user1.username
        password = "samplePassword123"
        
        result = create_user(username, password)
        self.assertIsNone(result)

    def test_create_by_invalid_password(self):
        username = "ausername"
        invalid_passwords = [
            "short",
            "sh0rt",
            "justletter",
            "1234587469852",
        ]

        for password in invalid_passwords:
            with self.assertRaises(ValidationError):
                create_user(username, password)
