```python
from django_app.models import User

class New_Email:
    def __init__(self, post_data, receivingList):
        # Initialize the email message, subject, and recipient list from the provided data
        self.message = post_data['message']
        self.subject = post_data['subject']
        self.recipients = receivingList
        self.statusMessage = 'Failed To Send! Check All Boxes'

    def get_subject(self):
        # Return the subject of the email
        return self.subject

    def get_message(self):
        # Return the message body of the email
        return self.message

    def get_recipients(self):
        # Return the list of recipients for the email
        return self.recipients

    def checkInfo(self):
        # Validate the email information before sending
        for email in self.recipients:
            if email is None or email.strip() == '':
                # If any recipient is missing, update status and return False
                self.statusMessage = f"Failed To Send Email! Missing Recipients"
                return False

        # Check if the subject line is empty
        if self.subject == '' or self.subject is None:
            self.statusMessage = "Failed To Send Email! Missing Subject Line"
            return False
        
        # Check if the message body is empty
        if self.message == '' or self.message is None:
            self.statusMessage = "Failed To Send Email! Missing Message Body"
            return False

        # If all checks pass, update status to indicate successful validation
        self.statusMessage = "Email Successfully Sent!"
        return True
```