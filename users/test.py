from django.test import TestCase
from django.db import IntegrityError
from users.models import User, UserProfile
from django.db import transaction
from users.api.user_profile.serializers import UserSignupSerializer, LoginSerializer
from rest_framework.exceptions import ValidationError

class UserModelTest(TestCase):
    
    def test_create_user(self):
        user = User.objects.create_user(username="testuser", password="testpass123")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(username="admin", password="adminpass123")
        self.assertEqual(superuser.username, "admin")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)

    def test_create_user_without_username_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(username=None, password="testpass123")

    def test_create_superuser_with_wrong_flags_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(username="admin2", password="adminpass123", is_staff=False)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(username="admin3", password="adminpass123", is_superuser=False)


class UserProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="profileuser", password="testpass123")

    def test_create_user_profile(self):
        profile = UserProfile.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone_number="+1234567890",
            gender="Male",
            date_of_birth="2000-01-01",
            address="123 Street"
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.first_name, "John")
        self.assertEqual(profile.email, "john@example.com")

    def test_user_profile_unique_email_and_phone(self):
        # Create first profile
        UserProfile.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            email="unique@example.com",
            phone_number="+1234567890"
        )

        # Duplicate email should raise IntegrityError
        user2 = User.objects.create_user(username="user2", password="pass123")
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                UserProfile.objects.create(
                    user=user2,
                    first_name="Jane",
                    last_name="Smith",
                    email="unique@example.com",
                    phone_number="+9876543210"
                )

        # Duplicate phone number should raise IntegrityError
        user3 = User.objects.create_user(username="user3", password="pass123")
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                UserProfile.objects.create(
                    user=user3,
                    first_name="Alice",
                    last_name="Smith",
                    email="alice@example.com",
                    phone_number="+1234567890"
                )





class UserSignupSerializerTest(TestCase):

    def setUp(self):
        self.valid_data = {
            "username": "newuser",
            "password": "strongpassword123",
            "profile": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "phone_number": "+1234567890",
                "gender": "Male",
                "date_of_birth": "2000-01-01",
                "address": "123 Street"
            }
        }

    def test_signup_creates_user_and_profile(self):
        serializer = UserSignupSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, self.valid_data["username"])
        self.assertTrue(user.check_password(self.valid_data["password"]))
        profile = user.user_profile
        self.assertEqual(profile.first_name, "John")
        self.assertEqual(profile.email, "john@example.com")

    def test_signup_duplicate_username_raises_error(self):
        # Create initial user
        User.objects.create_user(username="newuser", password="pass123")
        serializer = UserSignupSerializer(data=self.valid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class LoginSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="loginuser", password="loginpass123")

    def test_login_with_valid_credentials(self):
        data = {"username": "loginuser", "password": "loginpass123"}
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        result = serializer.validated_data
        self.assertEqual(result["username"], self.user.username)
        self.assertIsNotNone(result["access"])
        self.assertIsNotNone(result["refresh"])

    def test_login_invalid_username(self):
        data = {"username": "wronguser", "password": "loginpass123"}
        serializer = LoginSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_login_invalid_password(self):
        data = {"username": "loginuser", "password": "wrongpass"}
        serializer = LoginSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_login_disabled_account(self):
        self.user.is_active = False
        self.user.save()
        data = {"username": "loginuser", "password": "loginpass123"}
        serializer = LoginSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)