```python
from django_app.models import User
from datetime import datetime

def user_exists(user):
    """
    Check if a user with the given username exists in the database.
    
    Parameters:
        user (str): The username to check.
        
    Returns:
        bool: True if the user exists, False otherwise.
    """
    return User.objects.filter(user_name=user).exists()

# List of invalid characters for usernames
invalidCharacters = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '_', '+', '=', '!', '@', '#', '$', '%', '^', '&', '*', 
                     '(', ')', '{', '}', '[', ']', '~', '`', "'", '"', ';', ':', '?', '/', '|', '.', '>', '<', ',']

# List of special characters allowed in certain fields
specialCharacter = ['_', '+', '=', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '{', '}', '[', ']', '~', '`', "'", '"', ';', ':', '?', '/', '|', '.', '>', '<']

# List of valid roles
roles = ['TA', 'Instructor', 'Admin/Supervisor']


class WellFormed:
    """
    Class to validate user data for creation or update.
    
    Attributes:
        data (dict): Dictionary containing user information.
        customSTR (str): String indicating the action being performed ('Create' or 'Update').
        checkUser (bool): Flag to check if username exists.
        checkEmail (bool): Flag to check if email exists.
    """
    def __init__(self, username, password, confirm_password, firstName, lastName, email, phone1, phone2, phone3, street_address, city, state, zip_code, role, customSTR, checkUser, checkEmail):
        self.data = {
            'username': username,
            'password': password,
            'confirm_password': confirm_password,
            'first_name': firstName,
            'last_name': lastName,
            'email': email,
            'phone1': phone1,
            'phone2': phone2,
            'phone3': phone3,
            'street_address': street_address,
            'city': city,
            'state': state,
            'zip_code': zip_code,
            'role': role
        }
        self.customSTR = customSTR
        self.checkUser = checkUser
        self.checkEmail = checkEmail

    @property
    def check_user_information(self):
        """
        Validate the user information based on various criteria.
        
        Returns:
            tuple: (bool, str) - True if validation passes, False otherwise along with an error message.
        """
        min_length = 8
        max_length = 20

        # Check for missing information
        for key, value in self.data.items():
            if value is None or value.strip() == '':
                return False, f"Failed To {self.customSTR} User: Missing Information"

        # Validate password length and match
        if len(self.data['password']) < min_length or len(self.data['password']) > max_length:
            return False, f"Failed To {self.customSTR} User: Password Must Be Between 8 - 20 Characters"
        if self.data['password'] != self.data['confirm_password']:
            return False, f"Failed To {self.customSTR} User: Passwords Do Not Match"

        # Check for existing username
        if self.checkUser:
            if user_exists(self.data['username']):
                return False, f"Failed To {self.customSTR} User: That Username Is Already Used"

        # Validate phone number format
        if len(self.data['phone1']) != 3 or len(self.data['phone2']) != 3 or len(self.data['phone3']) != 4:
            return False, f"Failed To {self.customSTR} User: Invalid Phone Number"
        if not self.data['phone1'].isdigit() or not self.data['phone2'].isdigit() or not self.data['phone3'].isdigit():
            return False, f"Failed To {self.customSTR} User: Invalid Phone Number"

        # Validate zip code
        if len(self.data['zip_code']) != 5:
            return False, f"Failed To {self.customSTR} User: Invalid Zip Code"
        if not self.data['zip_code'].isdigit():
            return False, f"Failed To {self.customSTR} User: Invalid Zip Code"

        # Validate first name and last name for special characters
        if any(char in self.data['first_name'] for char in invalidCharacters):
            return False, f"Failed To {self.customSTR} User: Invalid First Name: Can Not Contain Special Characters"
        if any(char in self.data['last_name'] for char in invalidCharacters):
            return False, f"Failed To {self.customSTR} User: Invalid Last Name: Can Not Contain Special Characters"

        # Validate street address for special characters
        if any(char in self.data['street_address'] for char in specialCharacter):
            return False, f"Failed To {self.customSTR} User: Invalid Street Address: Can Not Contain Special Characters"

        # Validate city for special characters
        if any(char in self.data['city'] for char in invalidCharacters):
            return False, f"Failed To {self.customSTR} User: Invalid City: Can Not Contain Special Characters"

        # Check for existing email
        if self.checkEmail:
            if User.objects.filter(email_address=self.data['email']).exists():
                return False, f"Failed To {self.customSTR} User: Email Address Is Already Used"

        # Validate email format and domain
        if self.data['email'] == '@uwm.edu' or self.data['email'] == '@gmail.com' or len(self.data['email']) < min_length or (self.data['email'].find('@uwm.edu') == -1 and self.data['email'].find('@gmail.com') == -1):
            return False, f"Failed To {self.customSTR} User: Invalid Email Address"

        # Validate state
        if len(self.data['state']) != 2:
            return False, f"Failed To {self.customSTR} User: Invalid State"

        # Validate role
        if self.data['role'] not in roles:
            return False, f"Failed To {self.customSTR} User: Invalid Role"

        return True, "User data is valid"


class CreateUpdateBase:
    """
    Base class for creating or updating user information.
    
    Attributes:
        post_data (dict): Dictionary containing new user information.
        message (str): Message indicating the result of the operation.
    """
    def __init__(self, post_data):
        self.post_data = post_data
        self.message = 'Blank Error'

    def validate_and_save(self):
        """
        Validate and save the user information.
        
        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        try:
            well_formed_user = WellFormed(
                username=self.post_data['username'],
                password=self.post_data['password'],
                confirm_password=self.post_data['confirm_password'],
                firstName=self.post_data['first_name'],
                lastName=self.post_data['last_name'],
                email=self.post_data['email'],
                phone1=self.post_data['phone1'],
                phone2=self.post_data['phone2'],
                phone3=self.post_data['phone3'],
                street_address=self.post_data['street_address'],
                city=self.post_data['city'],
                state=self.post_data['state'],
                zip_code=self.post_data['zip_code'],
                role=self.post_data.get('role', 'User'),
                customSTR='Create',
                checkUser=True,
                checkEmail=True
            )
            is_valid, self.message = well_formed_user.check_user_information

            if not is_valid:
                return False

            phone_number = f"{self.post_data['phone1']}-{self.post_data['phone2']}-{self.post_data['phone3']}"

            user = User(
                username=self.post_data['username'],
                password=self.post_data['password'],
                first_name=self.post_data['first_name'],
                last_name=self.post_data['last_name'],
                email_address=self.post_data['email'],
                phone_number=phone_number,
                street_address=self.post_data['street_address'],
                city=self.post_data['city'],
                state=self.post_data['state'],
                zip_code=self.post_data['zip_code'],
                role_name=self.post_data.get('role', 'User')
            )
            user.save()
            self.message = "User created successfully"
            return True

        except Exception as e:
            self.message = f"Failed to create user: {str(e)}"
            return False


class UpdateUserInformation(Users):
    """
    Class to update user information.
    
    Attributes:
        post_data (dict): Dictionary containing new user information.
        message (str): Message indicating the result of the operation.
    """
    def __init__(self, post_data, user):
        super().__init__(user)
        self.post_data = post_data
        self.message = 'Blank Error'

    def update_information(self):
        """
        Update the user information with new data.
        
        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        checkEmail = self.get_email() != self.post_data['email']
        checkUser = False
        try:
            userRole = self.post_data['role']
        except KeyError:
            userRole = self.get_role_type()

        try:
            editUser = WellFormed(
                username=self.get_username(),
                password=self.post_data['password'],
                confirm_password=self.post_data['confirm_password'],
                firstName=self.post_data['first_name'],
                lastName=self.post_data['last_name'],
                email=self.post_data['email'],
                phone1=self.post_data['phone1'],
                phone2=self.post_data['phone2'],
                phone3=self.post_data['phone3'],
                street_address=self.post_data['street_address'],
                city=self.post_data['city'],
                state=self.post_data['state'],
                zip_code=self.post_data['zip_code'],
                role=userRole,
                customSTR='Update',
                checkUser=checkUser,
                checkEmail=checkEmail
            )
            is_valid, self.message = editUser.check_user_information

            if not is_valid:
                return False

            if self.__update_user(userRole):
                self.message = 'Successfully Updated User'
                return True
            else:
                return False

        except Exception as e:
            self.message = f"Failed to update user: {str(e)}"
            return False

    def __update_user(self, userRole):
        """
        Save the updated user information to the database.
        
        Parameters:
            userRole (str): The new role for the user.
            
        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        try:
            self.userData.password = self.post_data['password']
            self.userData.first_name = self.post_data['first_name']
            self.userData.last_name = self.post_data['last_name']
            self.userData.email_address = self.post_data['email']
            phone_number = f"{self.post_data['phone1']}-{self.post_data['phone2']}-{self.post_data['phone3']}"
            self.userData.phone_number = phone_number
            self.userData.street_address = self.post_data['street_address']
            self.userData.city = self.post_data['city']
            self.userData.state = self.post_data['state']
            self.userData.zip_code = self.post_data['zip_code']
            self.userData.role_name = userRole
            self.userData.save()
            return True

        except Exception as e:
            print(f"Error updating user: {str(e)}")
            return False

    def render_info(self):
        """
        Prepare information for rendering.
        
        Returns:
            dict: Dictionary containing user and additional context information.
        """
        render_info = self.get_all_context()
        render_info['state'] = User.USState
        render_info['role'] = User.Role
        render_info['current_role'] = self.get_role_type()
        render_info['current_state'] = self.get_state
        return render_info


class DisplayAllUsers:
    """
    Class to display all users.
    """
    def __init__(self):
        pass

    def get_users(self):
        """
        Retrieve all users from the database.
        
        Returns:
            QuerySet: A queryset containing all user records.
        """
        return User.objects.all()


class DeleteUser:
    """
    Class to delete a user.
    
    Attributes:
        user (Users): The user object to be deleted.
        message (str): Message indicating the result of the operation.
    """
    def __init__(self, user):
        self.user = Users(user)
        self.message = 'Blank Error'
        self.delete()

    def delete(self):
        """
        Delete the specified user from the database.
        """
        if self.user.is_user():
            User.objects.filter(user_name=self.user.get_username()).delete()
            self.message = "Successfully Deleted User"
        else:
            self.message = "Failed To Delete: Not A Valid User"
```

### Onboarding Documentation

#### Overview
This codebase provides a set of classes and functions to manage user data within a Django application. It includes functionality for creating, updating, displaying, and deleting users.

#### Classes
1. **WellFormed**
   - Validates user data based on various criteria such as password strength, username uniqueness, email format, phone number validation, etc.
   
2. **CreateUpdateBase**
   - Base class for handling the creation of new users. It includes methods to validate and save user information.

3. **Users**
   - Provides access to user details and basic operations like getting user data.

4. **UpdateUserInformation**
   - Extends `Users` to update existing user information. It validates the new data and saves it to the database if valid.

5. **DisplayAllUsers**
   - Allows retrieval of all users in the system.

6. **DeleteUser**
   - Handles the deletion of a specific user from the system.

#### Key Features
- **Validation**: Ensures that all user inputs meet specified criteria before saving them to the database.
- **Reusability**: Classes are designed to be reusable and can be extended for more complex operations if needed.
- **Error Handling**: Provides meaningful error messages in case of validation failures or database errors.

#### Usage
To create a new user, instantiate `CreateUpdateBase` with the necessary data. To update an existing user, use `UpdateUserInformation`. To display all users, use `DisplayAllUsers`, and to delete a user, use `DeleteUser`.

#### Dependencies
- **Django**: The codebase assumes that it is running within a Django environment where models are defined in `django_app.models`.
  
#### Installation
Ensure that your Django project is set up correctly with the necessary models for users. Install any required packages and then run your application.

This documentation provides a comprehensive overview of the classes, their functionalities, and how they interact to manage user data effectively within a Django application.