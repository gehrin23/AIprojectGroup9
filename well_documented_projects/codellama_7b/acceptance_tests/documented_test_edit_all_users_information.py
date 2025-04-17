The test cases are designed to verify that the `edit_user` view is functioning correctly and handling all possible input errors correctly. The test cases cover different scenarios such as passing invalid data, missing required fields, and incorrect values for various fields.

Here are some examples of what the tests might look like:

1. Testing with invalid data:
```python
def test_edit_user_invalid_data(self):
    # Create a user with a random username and password
    UserFactory()

    # Try to edit the user with invalid data
    response = self.client.post('/edit_user/', {
        'username': 'testuser',
        'password': 'invalid'
    })

    # Assert that the response is a redirect
    self.assertEqual(response.status_code, 302)
```
This test creates a user with a random username and password using the `UserFactory`. Then it tries to edit the user with invalid data (a password that is too short) by sending a POST request to the `/edit_user/` endpoint with the username and an invalid password. The response should be a redirect.

1. Testing missing required fields:
```python
def test_edit_user_missing_required_fields(self):
    # Create a user with a random username and password
    UserFactory()

    # Try to edit the user without required fields
    response = self.client.post('/edit_user/', {
        'username': '',
        'password': ''
    })

    # Assert that the response is a redirect
    self.assertEqual(response.status_code, 302)
```
This test creates a user with a random username and password using the `UserFactory`. Then it tries to edit the user without required fields (a blank username and password) by sending a POST request to the `/edit_user/` endpoint with no data. The response should be a redirect.

1. Testing incorrect values for various fields:
```python
def test_edit_user_incorrect_values(self):
    # Create a user with a random username and password
    UserFactory()

    # Try to edit the user with incorrect values for various fields
    response = self.client.post('/edit_user/', {
        'username': 'testuser12345',
        'password': 'invalid'
    })

    # Assert that the response is a redirect
    self.assertEqual(response.status_code, 302)
```
This test creates a user with a random username and password using the `UserFactory`. Then it tries to edit the user with incorrect values for various fields (a username that is too long and an invalid password). The response should be a redirect.

1. Testing existing usernames:
```python
def test_edit_user_existing_username(self):
    # Create two users with random usernames and passwords
    UserFactory()
    UserFactory()

    # Try to edit the second user with an existing username
    response = self.client.post('/edit_user/', {
        'username': 'testuser2',
        'password': 'invalid'
    })

    # Assert that the response is a redirect
    self.assertEqual(response.status_code, 302)
```
This test creates two users with random usernames and passwords using the `UserFactory`. Then it tries to edit the second user with an existing username (the same username as the first user). The response should be a redirect.