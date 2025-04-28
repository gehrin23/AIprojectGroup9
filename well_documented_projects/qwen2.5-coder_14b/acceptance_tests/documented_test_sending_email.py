```python
from django.test import TestCase, Client
from django_app.classes.email_class import New_Email
from django_app.models import User

class TestingSendingEmail(TestCase):
    user = None

    def setUp(self):
        self.user = Client()

        # Populate the User database with a test user
        User.objects.create(user_name='zackhawkins', password='zackhawkins', first_name='Zack', last_name='Hawkins', email_address='zhawkins@uwm.edu',
                           street_address='3072 N 75TH', city="Milwaukee", state='WI', zip_code='53210', phone_number='815-901-8423', role_name='Admin/Supervisor')

    # Test case to check if email sending fails due to missing recipients
    def test_missing_recipients(self):
        response = self.user.get('', {})
        self.assertTrue(response.status_code == 200)
        response = self.user.post('/login/', {'username': 'zackhawkins', 'password': 'zackhawkins'})
        self.assertRedirects(response, '/dashboard/')
        response = self.user.get('/send_email/', {})
        self.assertTrue(response.status_code == 200)
        recipientList = ['']
        response = self.user.post('/send_email/', {'message':'Hello Friends', 'subject':'Good Friends', 'recipients':recipientList})
        self.assertContains(response, 'Failed To Send Email! Missing Recipients')

    # Test case to check if email sending fails due to missing subject
    def test_missing_subject(self):
        response = self.user.get('', {})
        self.assertTrue(response.status_code == 200)
        response = self.user.post('/login/', {'username': 'zackhawkins', 'password': 'zackhawkins'})
        self.assertRedirects(response, '/dashboard/')
        response = self.user.get('/send_email/', {})
        self.assertTrue(response.status_code == 200)
        recipientList = ['zhawkins@uwm.edu']
        response = self.user.post('/send_email/', {'message':'Hello Friends', 'subject':'', 'recipients':recipientList})
        self.assertContains(response, 'Failed To Send Email! Missing Subject Line')

    # Test case to check if email sending fails due to missing message body
    def test_missing_message_body(self):
        response = self.user.get('', {})
        self.assertTrue(response.status_code == 200)
        response = self.user.post('/login/', {'username': 'zackhawkins', 'password': 'zackhawkins'})
        self.assertRedirects(response, '/dashboard/')
        response = self.user.get('/send_email/', {})
        self.assertTrue(response.status_code == 200)
        recipientList = ['zhawkins@uwm.edu']
        response = self.user.post('/send_email/', {'message':'', 'subject':'Good Friends', 'recipients':recipientList})
        self.assertContains(response, 'Failed To Send Email! Missing Message Body')

    # Test case to check if email sending is successful
    def test_sending_successful_email(self):
        response = self.user.get('', {})
        self.assertTrue(response.status_code == 200)
        response = self.user.post('/login/', {'username': 'zackhawkins', 'password': 'zackhawkins'})
        self.assertRedirects(response, '/dashboard/')
        response = self.user.get('/send_email/', {})
        self.assertTrue(response.status_code == 200)
        recipientList = ['zhawkins@uwm.edu']
        response = self.user.post('/send_email/', {'message':'Hello Friends', 'subject':'Good Friends', 'recipients':recipientList})
        self.assertContains(response, 'Email Successfully Sent!')
```

### Onboarding PDF Summary

#### 1. Overall File Purpose
This file contains unit tests for the email sending functionality in a Django application. It ensures that various scenarios related to email sending are handled correctly, including cases where required fields are missing and when the email is sent successfully.

#### 2. Key Functions/Methods and Their Responsibilities
- `setUp`: Initializes the test environment by creating a test user.
- `test_missing_recipients`: Tests the scenario where email sending fails due to missing recipients.
- `test_missing_subject`: Tests the scenario where email sending fails due to a missing subject line.
- `test_missing_message_body`: Tests the scenario where email sending fails due to a missing message body.
- `test_sending_successful_email`: Tests the scenario where an email is sent successfully.

#### 3. Inputs/Outputs/Side Effects
- **Inputs**: 
  - Test data for user creation and email sending.
- **Outputs**: 
  - Assertions checking HTTP status codes, redirects, and response content.
- **Side Effects**: 
  - Modifies the database by creating a test user.

#### 4. Design Patterns, Dependencies
- The test class `TestingSendingEmail` uses Django's built-in testing framework `TestCase`.
- It depends on the `Client` class for simulating HTTP requests and responses.
- It also depends on the `User` model and `New_Email` class from the application.

#### 5. Cohesion and Coupling
- **Cohesion**: High, as all test methods are related to testing email sending functionality within the same class.
- **Coupling**: Low, as the tests interact with Django's testing framework and database without relying on external systems or libraries beyond what is necessary for the tests.