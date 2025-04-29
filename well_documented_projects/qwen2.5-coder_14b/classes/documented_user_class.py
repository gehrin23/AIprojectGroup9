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

invalidCharacters =['1', '2', '3', '4', '5', '6', '7', '8', '9', '0','_', '+', '=', '!', '@', '#', '$', '%', '^', '&', '*',
        '(', ')', '{', '}', '[', ']', '~', '`', "'", '"', ';', ':', '?', '/', '|', '.', '>', '<', ',']

specialCharacter = ['_', '+', '=', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '{', '}', '[', ']', '~', '`', "'", '"', ';', ':', '?', '/', '|', '.', '>', '<']

roles = ['TA', 'Instructor', 'Admin/Supervisor']


class WellFormed:
    """
    Class to validate user information.

    Attributes:
    data (dict): Dictionary containing user details.
    customSTR (str): Custom string for error messages.
    checkUser (bool): Flag to check if username exists.
    checkEmail (bool): Flag to check if email exists.
    """

    def __init__(self, username, password, confirm_password, firstName, lastName, email, phone1, phone2, phone3, street_address, city, state, zip_code, role, customSTR, checkUser, checkEmail):
        self.data = {'username': username, 'password': password, 'confirm_password': confirm_password,
                    'first_name': firstName, 'last_name': lastName, 'email': email, 'phone1': phone1, 'phone2': phone2, 'phone3': phone3,
                    'street_address': street_address, 'city': city, 'state': state, 'zip_code': zip_code, 'role': role}
        self.customSTR = customSTR
        self.checkUser = checkUser
        self.checkEmail = checkEmail

    @property
    def check_user_information(self):
        """
        Validate user information.

        Returns:
        tuple: A tuple containing a boolean indicating validity and an error message if applicable.
        """
        min_length = 8
        max_length = 20
        for key, value in self.data.items():
            if value is None or value.strip() == '':
                return False, f"Failed To {self.customSTR} User: Missing Information"

        if len(self.data['password']) < min_length or len(self.data['password']) > max_length:
            return False, f"Failed To {self.customSTR} User: Password Must Be Between 8 - 20 Characters"

        if self.data['password'] != self.data['confirm_password']:
            return False, f"Failed To {self.customSTR} User: Passwords Do Not Match"

        if self.checkUser:
            if user_exists(self.data['username']):
                return False, f"Failed To {self.customSTR} User: That Username Is Already Used"

        if len(self.data['phone1']) != 3 or len(self.data['phone2']) != 3 or len(self.data['phone3']) != 4:
            return False, f"Failed To {self.customSTR} User: Invalid Phone Number"

        if not self.data['phone1'].isdigit() or not self.data['phone2'].isdigit() or not self.data['phone3'].isdigit():
            return False, f"Failed To {self.customSTR} User: Invalid Phone Number"

        if len(self.data['zip_code']) != 5:
            return False, f"Failed To {self.customSTR} User: Invalid Zip Code"

        if not self.data['zip_code'].isdigit():
            return False, f"Failed To {self.customSTR} User: Invalid Zip Code"

        if any(char in self.data['first_name'] for char in invalidCharacters):
            return False, f"Failed To {self.customSTR} User: Invalid First Name: Can Not Contain Special Characters"

        if any(char in self.data['last_name'] for char in invalidCharacters):
            return False, f"Failed To {self.customSTR} User: Invalid Last Name: Can Not Contain Special Characters"

        if any(char in self.data['email'] for char in specialCharacter):
            return False, f"Failed To {self.customSTR} User: Invalid Email: Can Not Contain Special Characters"

        if not self.data['role'].capitalize() in roles:
            return False, f"Failed To {self.customSTR} User: Invalid Role"

        return True, "Valid"


class CreateNewUser:
    """
    Class to create a new user.

    Attributes:
    post_data (dict): Dictionary containing user details.
    message (str): Message for error or success.
    """

    def __init__(self, post_data):
        self.post_data = post_data
        self.message = 'Blank Error'

    def create_user(self):
        """
        Create a new user after validation.

        Returns:
        bool: True if user is created successfully, False otherwise.
        """
        try:
            newUser = WellFormed(
                username=self.post_data['username'],
                password=self.post_data['password'],
                confirm_password=self.post_data['confirm_password'],
                firstName=self.post_data['firstName'],
                lastName=self.post_data['lastName'],
                email=self.post_data['email'],
                phone1=self.post_data['phone1'],
                phone2=self.post_data['phone2'],
                phone3=self.post_data['phone3'],
                street_address=self.post_data['street_address'],
                city=self.post_data['city'],
                state=self.post_data['state'],
                zip_code=self.post_data['zip_code'],
                role=self.post_data['role'],
                customSTR='Create',
                checkUser=True,
                checkEmail=True
            )
        except:
            self.message = "Failed To Create User: Missing Information"
            return False

        is_valid, message = newUser.check_user_information
        if not is_valid:
            self.message = message
            return False
        else:
            self.message = 'Successfully Created User'
            return self.__create_user()

    def __create_user(self):
        """
        Internal method to save the new user to the database.

        Returns:
        bool: True if user is created successfully, False otherwise.
        """
        try:
            User.objects.create(
                user_name=self.post_data['username'],
                password=self.post_data['password'],
                first_name=self.post_data['firstName'],
                last_name=self.post_data['lastName'],
                email_address=self.post_data['email'],
                phone_number=f"{self.post_data['phone1']}-{self.post_data['phone2']}-{self.post_data['phone3']}",
                street_address=self.post_data['street_address'],
                city=self.post_data['city'],
                state=self.post_data['state'],
                zip_code=self.post_data['zip_code'],
                role_name=self.post_data['role']
            )
            return True
        except:
            self.message = "Error Creating User! Re-check Information"
            return False


class Users:
    """
    Class to retrieve user information.

    Attributes:
    userData (User): The user object.
    """

    userData = None

    def __init__(self, user):
        try:
            self.userData = User.objects.get(user_name=user)
        except:
            pass

    def is_user(self):
        """
        Check if the user exists.

        Returns:
        bool: True if user exists, False otherwise.
        """
        return self.userData is not None

    def get_all_context(self):
        """
        Get all user information in a dictionary format.

        Returns:
        dict: Dictionary containing user details.
        """
        phone1, phone2, phone3 = self.userData.phone_number.split('-')
        return {
            'username': self.userData.user_name,
            'password': self.userData.password,
            'first_name': self.userData.first_name,
            'last_name': self.userData.last_name,
            'email': self.userData.email_address,
            'phone1': phone1,
            'phone2': phone2,
            'phone3': phone3,
            'street_address': self.userData.street_address,
            'city': self.userData.city,
            'state': self.userData.state,
            'zip_code': self.userData.zip_code,
            'role': self.userData.role_name
        }

    def get_username(self):
        """
        Get the username of the user.

        Returns:
        str: The username.
        """
        return self.userData.user_name

    def get_password(self):
        """
        Get the password of the user.

        Returns:
        str: The password.
        """
        return self.userData.password

    def get_firstName(self):
        """
        Get the first name of the user.

        Returns:
        str: The first name.
        """
        return self.userData.first_name

    def get_lastName(self):
        """
        Get the last name of the user.

        Returns:
        str: The last name.
        """
        return self.userData.last_name

    def get_full_name(self):
        """
        Get the full name of the user.

        Returns:
        str: The full name.
        """
        return f'{self.userData.first_name} {self.userData.last_name}'

    def get_email(self):
        """
        Get the email address of the user.

        Returns:
        str: The email address.
        """
        return self.userData.email_address

    def get_home_address(self):
        """
        Get the home address of the user.

        Returns:
        str: The home address.
        """
        return f'{self.userData.street_address}, {self.userData.city}, {self.userData.state}, {self.userData.zip_code}'

    def get_street_address(self):
        """
        Get the street address of the user.

        Returns:
        str: The street address.
        """
        return self.userData.street_address

    def get_city(self):
        """
        Get the city of the user.

        Returns:
        str: The city.
        """
        return self.userData.city

    def get_state(self):
        """
        Get the state of the user.

        Returns:
        str: The state.
        """
        return self.userData.state

    def get_zip_code(self):
        """
        Get the zip code of the user.

        Returns:
        str: The zip code.
        """
        return self.userData.zip_code

    def get_phone_number(self):
        """
        Get the phone number of the user.

        Returns:
        str: The phone number.
        """
        return self.userData.phone_number

    def get_role_type(self):
        """
        Get the role type of the user.

        Returns:
        str: The role type.
        """
        return self.userData.role_name


class UpdateUserInformation(Users):
    """
    Class to update user information.

    Attributes:
    post_data (dict): Dictionary containing new user details.
    message (str): Message for error or success.
    """

    def __init__(self, post_data, user):
        super().__init__(user)
        self.post_data = post_data
        self.message = 'Blank Error'

    def update_information(self):
        """
        Update user information after validation.

        Returns:
        bool: True if user is updated successfully, False otherwise.
        """
        checkEmail = self.get_email() != self.post_data['email']
        checkUser = False
        try:
            userRole = self.post_data['role']
        except:
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
        except:
            self.message = "Failed To Update User: Missing Information"
            return False

        is_valid, message = editUser.check_user_information
        if not is_valid:
            self.message = message
            return False
        else:
            self.message = 'Successfully Updated User'
            return self.__update_user(userRole)

    def __update_user(self, userRole):
        """
        Internal method to save the updated user information to the database.

        Returns:
        bool: True if user is updated successfully, False otherwise.
        """
        try:
            self.userData.password = self.post_data['password']
            self.userData.first_name = self.post_data['first_name']
            self.userData.last_name = self.post_data['last_name']
            self.userData.email_address = self.post_data['email']
            phone = f"{self.post_data['phone1']}-{self.post_data['phone2']}-{self.post_data['phone3']}"
            self.userData.phone_number = phone
            self.userData.street_address = self.post_data['street_address']
            self.userData.city = self.post_data['city']
            self.userData.state = self.post_data['state']
            self.userData.zip_code = self.post_data['zip_code']
            self.userData.role_name = userRole
            self.userData.save()
            return True
        except:
            self.message = "Failed To Update User: Missing Information"
            return False

    def render_info(self):
        """
        Render the update information.

        Returns:
        dict: Dictionary containing all user details.
        """
        render_info = self.get_all_context()
        render_info['state'] = User.USState
        render_info['role'] = User.Role
        render_info['current_role'] = self.get_role_type
        render_info['current_state'] = self.get_state
        return render_info


class DisplayAllUsers:
    """
    Class to display all users.

    Attributes:
    user_list (list): List of all users.
    """

    def __init__(self):
        self.user_list = User.objects.all()

    def get_users(self):
        """
        Get a list of all users.

        Returns:
        QuerySet: A queryset of all users.
        """
        return self.user_list


class DeleteUser:
    """
    Class to delete a user.

    Attributes:
    username (str): The username of the user to be deleted.
    message (str): Message for error or success.
    """

    def __init__(self, username):
        self.username = username
        self.message = 'Blank Error'

    def delete(self):
        """
        Delete a user.

        Returns:
        bool: True if user is deleted successfully, False otherwise.
        """
        try:
            user_to_delete = User.objects.get(user_name=self.username)
            user_to_delete.delete()
            self.message = 'Successfully Deleted User'
            return True
        except User.DoesNotExist:
            self.message = 'User Not Found'
            return False
        except Exception as e:
            self.message = f'Error Deleting User: {str(e)}'
            return False


class SearchUsers:
    """
    Class to search for users.

    Attributes:
    query (str): The search query.
    user_list (list): List of matching users.
    """

    def __init__(self, query):
        self.query = query
        self.user_list = []

    def search(self):
        """
        Search for users based on the provided query.

        Returns:
        QuerySet: A queryset of matching users.
        """
        if self.query:
            self.user_list = User.objects.filter(
                Q(user_name__icontains=self.query) |
                Q(first_name__icontains=self.query) |
                Q(last_name__icontains=self.query) |
                Q(email_address__icontains=self.query)
            )
        return self.user_list
```