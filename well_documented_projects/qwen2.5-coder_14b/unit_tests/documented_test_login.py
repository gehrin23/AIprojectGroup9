```python
from django.test import TestCase
from django_app.models import User
from django_app.classes.login import LoginHandler

class LoginHandlerTestCase(TestCase):

    # Setup method to create a test user before each test case
    def setUp(self):
        self.test_user = User.objects.create(
            user_name="testuser",
            password="password123",
            first_name="Test",
            last_name="User",
            email_address="test@example.com",
            street_address="123 Test St",
            city="Milwaukee",
            state="WI",
            zip_code="12345",
            phone_number="123-456-7890",
            role_name="TA"
        )

    # Test case to validate user with correct credentials
    def test_validate_user_valid(self):
        request_data = {
            "username": "testuser",
            "password": "password123"
        }
        login_handler = LoginHandler(request_data)
        self.assertTrue(login_handler.validate_user())  # Validate that the user is authenticated
        self.assertEqual(login_handler.role, "TA")  # Check if the role is correctly assigned

    # Test case to validate user with incorrect credentials
    def test_validate_user_invalid(self):
        request_data = {
            "username": "wronguser",
            "password": "wrongpassword"
        }
        login_handler = LoginHandler(request_data)
        self.assertFalse(login_handler.validate_user())  # Validate that the user is not authenticated

    # Test case to check the redirect URL based on user role
    def test_get_redirect_url(self):
        request_data = {
            "username": "testuser",
            "password": "password123"
        }
        login_handler = LoginHandler(request_data)
        login_handler.validate_user()
        self.assertEqual(login_handler.get_redirect_url(), "/dashboard/")  # Check redirect URL for TA role

        self.test_user.role_name = "Admin/Supervisor"  # Change user role to Admin/Supervisor
        self.test_user.save()
        login_handler = LoginHandler(request_data)
        login_handler.validate_user()
        self.assertEqual(login_handler.get_redirect_url(), "/dashboard/")  # Check redirect URL for Admin/Supervisor role

    # Cleanup method to delete all test users after each test case
    def tearDown(self):
        User.objects.all().delete()
```