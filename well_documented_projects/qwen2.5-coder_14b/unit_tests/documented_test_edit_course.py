```python
from django.test import TestCase, RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from django.urls import reverse

from django_app.models import Course
from django_app.views import Edit_Course


class TestEditCourseView(TestCase):
    def setUp(self):
        # Initialize the RequestFactory for creating test requests
        self.factory = RequestFactory()
        # Create a sample course instance to use in tests
        self.course = Course.objects.create(
            courseId="CSE101",
            courseName="Intro to Computer Science",
            credits=3,
            startDate="2024-01-01",
            endDate="2024-05-01"
        )

    def setup_request_with_messages(self, method, url, data=None):
        """
        Create a test request with messages middleware.

        :param method: HTTP method ('GET' or 'POST')
        :param url: URL to which the request is sent
        :param data: Data for POST requests (optional)
        :return: Configured request object
        """
        if method == 'POST':
            # Create a POST request with given data
            request = self.factory.post(url, data)
        else:
            # Create a GET request
            request = self.factory.get(url)
        # Set up session and messages middleware for the request
        request.session = {}
        request._messages = FallbackStorage(request)
        return request

    def test_get_edit_course(self):
        """Test GET request to edit course."""
        url = reverse('edit_course', args=[self.course.courseId])
        request = self.setup_request_with_messages('GET', url)
        response = Edit_Course.as_view()(request, courseId=self.course.courseId)
        # Verify that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Ensure the course name is present in the response
        self.assertContains(response, "Intro to Computer Science")

    def test_post_delete_course(self):
        """Test POST request to delete course."""
        url = reverse('edit_course', args=[self.course.courseId])
        data = {'action': 'delete'}
        request = self.setup_request_with_messages('POST', url, data)
        response = Edit_Course.as_view()(request, courseId=self.course.courseId)
        # Verify that the course no longer exists in the database
        with self.assertRaises(Course.DoesNotExist):
            Course.objects.get(courseId=self.course.courseId)
```

### Onboarding PDF Summary

#### Overall File Purpose
This file contains unit tests for the `Edit_Course` view in a Django application. The primary goal is to ensure that both GET and POST requests function correctly, specifically focusing on editing and deleting courses.

#### Key Functions/Methods and Their Responsibilities
1. **setUp(self)**: Initializes the RequestFactory for creating test requests and sets up a sample course instance.
2. **setup_request_with_messages(self, method, url, data=None)**: Creates a test request with messages middleware, handling both GET and POST methods.
3. **test_get_edit_course(self)**: Tests the GET request to edit a course, ensuring the response status code is 200 and that the course name is present in the response.
4. **test_post_delete_course(self)**: Tests the POST request to delete a course, verifying that the course no longer exists in the database.

#### Inputs/Outputs/Side Effects
- **Inputs**: HTTP method ('GET' or 'POST'), URL, and optional data for POST requests.
- **Outputs**: Test results indicating whether the view behaves as expected.
- **Side Effects**: Creates and deletes a course instance during test execution.

#### Design Patterns, Dependencies
- **Design Pattern**: Unit Testing with Django's TestCase framework.
- **Dependencies**:
  - Django's `TestCase` and `RequestFactory`.
  - `Course` model from `django_app.models`.
  - `Edit_Course` view from `django_app.views`.

#### Cohesion and Coupling
- **Cohesion**: High cohesion within the test class, as all methods are related to testing the `Edit_Course` view.
- **Coupling**: Low coupling, as the tests primarily interact with the Django framework's testing tools and the `Course` model without relying on external systems.