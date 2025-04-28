```python
from django_app.models import User

class New_Email:
    def __init__(self, post_data, receivingList):
        """
        Initializes a new email instance with the given message, subject, and list of recipients.

        :param post_data: A dictionary containing 'message' and 'subject' keys.
        :param receivingList: A list of recipient email addresses.
        """
        self.message = post_data['message']
        self.subject = post_data['subject']
        self.recipients = receivingList
        self.statusMessage = 'Failed To Send! Check All Boxes'

    def get_subject(self):
        """
        Returns the subject of the email.

        :return: The subject string.
        """
        return self.subject

    def get_message(self):
        """
        Returns the message body of the email.

        :return: The message string.
        """
        return self.message

    def get_recipients(self):
        """
        Returns the list of recipient email addresses.

        :return: A list of email addresses.
        """
        return self.recipients

    def checkInfo(self):
        """
        Validates the email details to ensure that all necessary fields are filled out.

        :return: True if the email information is valid, False otherwise.
        """
        for email in self.recipients:
            # Check if any recipient email is None or empty
            if email is None or email.strip() == '':
                self.statusMessage = f"Failed To Send Email! Missing Recipients"
                return False

        # Check if the subject is missing
        if self.subject == '' or self.subject is None:
            self.statusMessage = "Failed To Send Email! Missing Subject Line"
            return False
        
        # Check if the message body is missing
        if self.message == '' or self.message is None:
            self.statusMessage = "Failed To Send Email! Missing Message Body"
            return False

        # Set status to success if all checks pass
        self.statusMessage = "Email Successfully Sent!"
        return True
```

### Onboarding PDF Summary:

#### 1. Overall File Purpose
This file defines a class `New_Email` designed to handle the creation and validation of email messages within a Django application. It ensures that all required fields (message, subject, and recipients) are properly filled out before attempting to send an email.

#### 2. Key Functions/Methods and Their Responsibilities
- **`__init__(self, post_data, receivingList)`**: Initializes the email object with data from `post_data` and a list of recipient emails.
- **`get_subject(self)`**: Returns the subject of the email.
- **`get_message(self)`**: Returns the message body of the email.
- **`get_recipients(self)`**: Returns the list of recipient email addresses.
- **`checkInfo(self)`**: Validates the email details to ensure that all necessary fields are filled out.

#### 3. Inputs/Outputs/Side Effects
- **Inputs**:
  - `post_data`: A dictionary containing 'message' and 'subject' keys.
  - `receivingList`: A list of recipient email addresses.
- **Outputs**:
  - Methods return the respective values for subject, message, and recipients.
  - The `checkInfo` method returns a boolean indicating whether the email details are valid.
- **Side Effects**:
  - Updates the `statusMessage` attribute based on the validation result.

#### 4. Design Patterns, Dependencies
- **Design Pattern**: Encapsulation - The class encapsulates all the necessary data and methods for creating and validating an email.
- **Dependencies**:
  - `django_app.models.User`: Although not directly used in this file, it indicates that the Django application's models are utilized elsewhere.

#### 5. Point Out Cohesion and Coupling
- **Cohesion**: High - All methods within the class are focused on handling and validating email data.
- **Coupling**: Low - The class is self-contained and does not rely on external dependencies beyond the necessary imports for its functionality.