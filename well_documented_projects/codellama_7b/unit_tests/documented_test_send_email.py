Here is the revised code with inline comments and docstrings added where necessary:
```
from django_app.classes.email_class import New_Email
from django.test import TestCase

class TestEmailSending(TestCase):
    """
    Class for testing email sending functionality in the New_Email class.
    """

    def test_missing_message_box(self):
        """
        Test case for missing message body.
        """
        list = ['zackhawkins@gmail.com']
        data = {'message': '', 'subject': 'Saying Hi'}
        email = New_Email(data, list)
        self.assertFalse(email.checkInfo())
        self.assertEqual(email.statusMessage, "Failed To Send Email! Missing Message Body")

    def test_missing_subject(self):
        """
        Test case for missing subject line.
        """
        list = ['zackhawkins@gmail.com']
        data = {'message': 'Hello my fellow friends', 'subject': ''}
        email = New_Email(data, list)
        self.assertFalse(email.checkInfo())
        self.assertEqual(email.statusMessage, "Failed To Send Email! Missing Subject Line")

    def test_missing_recipients(self):
        """
        Test case for missing recipients.
        """
        list = ['']
        data = {'message': '', 'subject': 'Saying Hi'}
        email = New_Email(data, list)
        self.assertFalse(email.checkInfo())
        self.assertEqual(email.statusMessage, "Failed To Send Email! Missing Recipients")

    def test_successful_sending_email(self):
        """
        Test case for successful email sending.
        """
        list = ['zackhawkins@gmail.com']
        data = {'message': 'Hello Friends I am your friend', 'subject': 'Saying Hi'}
        email = New_Email(data, list)
        self.assertTrue(email.checkInfo())
        self.assertEqual(email.statusMessage, "Email Successfully Sent!")
```
Overall file purpose: This class is used for testing the functionality of the New_Email class in the django_app.classes module. It includes test cases for missing message body, subject line, recipients, and successful email sending.

Key functions/methods and their responsibilities:

* `test_missing_message_box`: Test case for missing message body.
* `test_missing_subject`: Test case for missing subject line.
* `test_missing_recipients`: Test case for missing recipients.
* `test_successful_sending_email`: Test case for successful email sending.

Inputs/outputs/side effects:

* Inputs: list of recipients, dictionary with message and subject keys.
* Outputs: statusMessage (string) indicating the result of email sending.
* Side effects: None.

Design patterns, dependencies:

* Depends on the New_Email class from django_app.classes.email_class module.
* Uses the TestCase class from Django's testing framework for writing test cases.

Cohesion and coupling:

* Cohesion: High. The methods in this class are focused on testing specific functionality of the New_Email class, and do not have dependencies on other classes or modules outside of the current module.
* Coupling: Low. This class has a loose coupling with the New_Email class as it only depends on the interface provided by the class. It does not have any hardcoded dependencies on the implementation details of the class.