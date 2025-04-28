```python
from django_app.classes.email_class import New_Email
from django.test import TestCase

class TestEmailSending(TestCase):

    #-----------------------------------------Failed Sending Email-----------------------------------------#
    
    def test_missing_message_box(self):
        """
        Tests the scenario where an email is sent without a message body.
        
        Asserts that:
        - The `checkInfo` method returns False indicating invalid email info.
        - The status message reflects missing message body.
        """
        list = ['zackhawkins@gmail.com']
        data = {'message':'', 'subject':'Saying Hi'}
        email = New_Email(data, list)
        self.assertFalse(email.checkInfo())
        self.assertEqual(email.statusMessage, "Failed To Send Email! Missing Message Body")

    def test_missing_subject(self):
        """
        Tests the scenario where an email is sent without a subject line.
        
        Asserts that:
        - The `checkInfo` method returns False indicating invalid email info.
        - The status message reflects missing subject line.
        """
        list = ['zackhawkins@gmail.com']
        data = {'message':'Hello my fellow friends', 'subject':''}
        email = New_Email(data, list)
        self.assertFalse(email.checkInfo())
        self.assertEqual(email.statusMessage, "Failed To Send Email! Missing Subject Line")

    def test_missing_recipients(self):
        """
        Tests the scenario where an email is sent without any recipients.
        
        Asserts that:
        - The `checkInfo` method returns False indicating invalid email info.
        - The status message reflects missing recipients.
        """
        list = ['']
        data = {'message':'', 'subject':'Saying Hi'}
        email = New_Email(data, list)
        self.assertFalse(email.checkInfo())
        self.assertEqual(email.statusMessage, "Failed To Send Email! Missing Recipients")

    #-----------------------------------------Successful Sending Email-----------------------------------------#

    def test_successful_sending_email(self):
        """
        Tests the scenario where an email is sent successfully with all required fields.
        
        Asserts that:
        - The `checkInfo` method returns True indicating valid email info.
        - The status message reflects successful email sending.
        """
        list = ['zackhawkins@gmail.com']
        data = {'message':'Hello Friends I am your friend', 'subject':'Saying Hi'}
        email = New_Email(data, list)
        self.assertTrue(email.checkInfo())
        self.assertEqual(email.statusMessage, "Email Successfully Sent!")
```

**Onboarding PDF Summary:**

1. **Overall File Purpose:**
   - The file contains unit tests for the `New_Email` class in a Django application. It specifically focuses on testing scenarios where email sending might fail due to missing information and scenarios where email sending is successful.

2. **Key Functions/Methods and Their Responsibilities:**
   - `test_missing_message_box`: Tests if an email can be sent without a message body.
   - `test_missing_subject`: Tests if an email can be sent without a subject line.
   - `test_missing_recipients`: Tests if an email can be sent without any recipients.
   - `test_successful_sending_email`: Tests if an email can be sent successfully with all required fields.

3. **Inputs/Outputs/Side Effects:**
   - **Inputs:** 
     - List of recipient emails.
     - Data dictionary containing message and subject.
   - **Outputs:** 
     - Asserts that the `checkInfo` method returns appropriate boolean values based on input validity.
     - Asserts that the `statusMessage` reflects the correct status (success or failure) after attempting to send the email.

4. **Design Patterns, Dependencies:**
   - The code follows a unit testing pattern using Django's `TestCase`.
   - It depends on the `New_Email` class from `django_app.classes.email_class`.

5. **Cohesion and Coupling:**
   - **Cohesion:** High, as all methods are related to testing email sending scenarios.
   - **Coupling:** Low, as each test method is independent and only relies on the `New_Email` class for functionality.