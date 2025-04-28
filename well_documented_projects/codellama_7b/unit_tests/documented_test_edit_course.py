Here is the revised code with inline comments and docstrings added where necessary:
```
from django.test import TestCase, RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from django.urls import reverse

from django_app.models import Course
from django_app.views import Edit_Course


class TestEditCourseView(TestCase):
    """Class for testing the Edit Course view."""
    
    def setUp(self):
        self.factory = RequestFactory()
        self.course = Course.objects.create(
            courseId="CSE101",
            courseName="Intro to Computer Science",
            credits=3,
            startDate="2024-01-01",
            endDate="2024-05-01"
        )

    def setup_request_with_messages(self, method, url, data=None):
        """Sets up a request with messages for the Edit Course view."""
        if method == 'POST':
            request = self.factory.post(url, data)
        else:
            request = self.factory.get(url)
        request.session = {}
        request._messages = FallbackStorage(request)
        return request

    def test_get_edit_course(self):
        """Tests the GET request to edit a course."""
        url = reverse('edit_course', args=[self.course.courseId])
        request = self.setup_request_with_messages('GET', url)
        response = Edit_Course.as_view()(request, courseId=self.course.courseId)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Intro to Computer Science")

    def test_post_delete_course(self):
        """Tests the POST request to delete a course."""
        url = reverse('edit_course', args=[self.course.courseId])
        data = {'action': 'delete'}
        request = self.setup_request_with_messages('POST', url, data)
        response = Edit_Course.as_view()(request, courseId=self.course.courseId)
        with self.assertRaises(Course.DoesNotExist):
            Course.objects.get(courseId=self.course.courseId)
```
Overall file purpose: The overall purpose of this file is to test the Edit Course view in the django_app application. It contains tests for both GET and POST requests to edit a course.

Key functions/methods and their responsibilities:

* setUp(): This method sets up the necessary fixtures for the tests, including creating a course object.
* setup_request_with_messages(): This method sets up a request with messages for the Edit Course view.
* test_get_edit_course(): This method tests the GET request to edit a course by checking the response status code and containing the course name.
* test_post_delete_course(): This method tests the POST request to delete a course by checking that the course no longer exists in the database.

Inputs/outputs/side effects:

* Inputs: GET or POST requests to the Edit Course view with the course ID.
* Outputs: The response status code and the course name for the GET request, and the deleted course object for the POST request.
* Side effects: Creates a new course object and deletes an existing course object if a POST request is made.

Design patterns, dependencies:

* Factory pattern: Used to create the course object in the setUp() method.
* Service locator pattern: Used to get the Edit Course view in the test methods.
* Dependency injection: Used to inject the course object into the test methods as a fixture.

Cohesion and coupling:

* Cohesion: High, the class is cohesive since all of its tests are related to the Edit Course view.
* Coupling: Low, the class has low coupling since it only depends on the TestCase class from Django's test framework.