Here is the documentation for the provided test suite:

**Test Suite:** `create_user_test_suite`

This test suite consists of 34 tests that cover various scenarios for creating a new user. The tests are divided into several categories:

1. **Valid User Creation**: Tests that create a new user with valid data.
2. **Invalid Email**: Tests that attempt to create a new user with an invalid email address (e.g., missing "@", incorrect domain).
3. **Invalid Password**: Tests that attempt to create a new user with an invalid password (e.g., too short, missing characters).
4. **Invalid First Name**: Tests that attempt to create a new user with an invalid first name (e.g., too long, special characters).
5. **Invalid Last Name**: Tests that attempt to create a new user with an invalid last name (e.g., too long, special characters).
6. **Invalid Phone Number**: Tests that attempt to create a new user with an invalid phone number (e.g., missing area code, incorrect formatting).
7. **Invalid Street Address**: Tests that attempt to create a new user with an invalid street address (e.g., missing city, incorrect formatting).
8. **Invalid City**: Tests that attempt to create a new user with an invalid city (e.g., missing state, incorrect formatting).
9. **Invalid State**: Tests that attempt to create a new user with an invalid state (e.g., missing zip code, incorrect abbreviation).
10. **Invalid Zip Code**: Tests that attempt to create a new user with an invalid zip code (e.g., missing leading zeros, incorrect formatting).
11. **Invalid Role**: Tests that attempt to create a new user with an invalid role (e.g., unknown role, role not in the expected format).

Each test case is designed to test a specific scenario and verifies that the expected outcome occurs. The `tearDown` method is used to ensure that any temporary data created during testing is cleaned up after each test.

**Example Test:**

```
def test_create_user_bad_zipCode1(self):
    newUser = CreateUsers({'username':'zackhawkins', 'password':'zackhawkins', 'confirm_password':'zackhawkins', 'first_name':'Zack', 'last_name':'Hawkins', 'email':'zhawkins@uwm.edu',
                        'phone1':'815', 'phone2':'901', 'phone3':'8423', 'street_address':'3072 N 75TH', 'city':'Milwaukee', 'state':'WI', 'zip_code':'6115', 'role':'Admin'})
    self.assertFalse(newUser.new_user())
    self.assertEqual(newUser.message, 'Failed To Create User: Invalid Zip Code')
```

In this example test, we create a new user with an invalid zip code ("6115") and verify that the expected outcome occurs (i.e., the user is not created and the message "Failed To Create User: Invalid Zip Code" is returned).