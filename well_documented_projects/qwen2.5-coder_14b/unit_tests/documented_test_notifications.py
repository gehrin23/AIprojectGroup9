```python
from django.test import TestCase
from django.http import HttpRequest
from django.urls import reverse
from django_app.models import Notification
from django_app.views import Notifications, DeleteNotification


class TestNotificationsView(TestCase):
    def setUp(self):
        # Create test notifications for the test cases
        self.notification_1 = Notification.objects.create(message="Test Notification 1", role="Admin/Supervisor")
        self.notification_2 = Notification.objects.create(message="Test Notification 2", role="Instructor")

    def test_get_notifications(self):
        """
        Test the GET method of the Notifications view.
        Ensures that notifications are rendered correctly in the response.
        """
        view = Notifications()
        request = HttpRequest()
        request.method = "GET"

        response = view.get(request)

        # Verify that the response is successful
        self.assertEqual(response.status_code, 200)

        # Render template to string and verify that notifications context is present
        rendered_content = response.content.decode("utf-8")
        self.assertIn(self.notification_1.message, rendered_content)
        self.assertIn(self.notification_2.message, rendered_content)

    def test_post_notifications(self):
        """
        Test the POST method of the Notifications view.
        Ensures that a new notification is created and redirects to the notifications page.
        """
        view = Notifications()
        request = HttpRequest()
        request.method = "POST"
        request.POST = {
            "message": "New Notification",
            "role": "TA"
        }

        response = view.post(request)

        # Check that the notification was successfully created
        self.assertTrue(Notification.objects.filter(message="New Notification", role="TA").exists())

        # Check for redirect after successful creation
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/notifications/")


class TestDeleteNotificationView(TestCase):
    def setUp(self):
        # Create a test notification for the delete test case
        self.notification = Notification.objects.create(message="Delete Me", role="Admin/Supervisor")

    def test_post_delete_notification(self):
        """
        Test the POST method of the DeleteNotification view.
        Ensures that a notification is deleted and redirects to the notifications page.
        """
        view = DeleteNotification()
        request = HttpRequest()
        request.method = "POST"
        request.POST = {}

        # Pass the notification ID to the view
        response = view.post(request, notification_id=self.notification.id)

        # Check that the notification was successfully deleted
        self.assertFalse(Notification.objects.filter(id=self.notification.id).exists())

        # Check for redirect after successful deletion
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/notifications/")
```