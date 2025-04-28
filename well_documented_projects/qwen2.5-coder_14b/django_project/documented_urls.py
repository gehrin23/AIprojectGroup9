```python
"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django_app.views import (
    LandingPage,
    Login,
    Dashboard,
    Create_User,
    Create_Course,
    Update_Personnel_Information,
    Logout,
    Calendar,
    Notifications,
    DeleteNotification,
    Tasks,
    Display_All_Users,
    Assign_User,
    Create_Section,
    Edit_Section,
    Edit_Course,
    Manage_Courses_Sections,
    ViewTAAssignments,
    DeleteTask,
    EditUsers,
    ContactCard,
    Delete_User,
    Email,
)

urlpatterns = [
    path('_debug_', include('debug_toolbar.urls')),  # django debug tool
    path('admin/', admin.site.urls),  # django admin portal
    path('', LandingPage.as_view(), name='landing_page'),  # Landing Page
    path('login/', Login.as_view(), name='login'),  # Login Page
    path('dashboard/', Dashboard.as_view(), name='dashboard'),  # Dashboard
    path('create_user/', Create_User.as_view(), name='create_user'),  # Create User
    path('create_course/', Create_Course.as_view(), name='create_course'),  # Create Course
    path('edit_personnel_info/', Update_Personnel_Information.as_view(), name='edit_personnel_info'),  # Edit Personnel Information
    path('logout/', Logout.as_view(), name='logout'),  # Logout From Webpage
    path('calendar/', Calendar.as_view(), name='calendar'),  # Calendar
    path('notifications/', Notifications.as_view(), name='notifications'),
    path('notifications/create/', Notifications.as_view(), name='create_notification'),
    path('notifications/delete/<int:notification_id>/', DeleteNotification.as_view(), name='delete_notification'),
    path('tasks/', Tasks.as_view(), name='tasks'),  # Tasks
    path('display_all_users/', Display_All_Users.as_view(), name='display_all_users'),  # Display All Active Users
    path('assign_user/', Assign_User.as_view(), name='assign_user'),  # Assign User Page
    path('create_section/', Create_Section.as_view(), name='create_section'),  # Create Section
    path('edit_section/<str:sectionId>/', Edit_Section.as_view(), name='edit_section'),
    path('edit_course/<str:courseId>/', Edit_Course.as_view(), name='edit_course'),  # Add courseId parameter
    path('manage_courses_sections/', Manage_Courses_Sections.as_view(), name='manage_courses_sections'),  # Manage Courses/Sections
    path('assignments/', ViewTAAssignments.as_view(), name="view_ta_assignments"),  # View TA Assignments
    path('tasks/delete/<int:task_id>/', DeleteTask.as_view(), name='delete_task'),  # Delete Task
    path('edit_user_info/', EditUsers.as_view(), name='edit_user_info'),  # Edit User Information
    path('user_contact_card/', ContactCard.as_view(), name='contact_card'),  # User Contact Card
    path('delete_user', Delete_User.as_view(), name='delete_user'),  # Delete User
    path('send_email/', Email.as_view(), name='send_email'),  # Send Email
]
```

### Onboarding PDF Summary

#### 1. Overall File Purpose
This file contains the URL configuration for the `django_project` project. It maps URLs to their corresponding views, allowing users to navigate through different functionalities of the application.

#### 2. Key Functions/Methods and Their Responsibilities
- **path('admin/', admin.site.urls)**: Provides access to the Django admin portal.
- **path('', LandingPage.as_view(), name='landing_page')**: Displays the landing page.
- **path('login/', Login.as_view(), name='login')**: Handles user login.
- **path('dashboard/', Dashboard.as_view(), name='dashboard')**: Shows the dashboard for logged-in users.
- **path('create_user/', Create_User.as_view(), name='create_user')**: Allows creating a new user.
- **path('create_course/', Create_Course.as_view(), name='create_course')**: Enables creation of a new course.
- **path('edit_personnel_info/', Update_Personnel_Information.as_view(), name='edit_personnel_info')**: Lets users edit their personnel information.
- **path('logout/', Logout.as_view(), name='logout')**: Handles user logout.
- **path('calendar/', Calendar.as_view(), name='calendar')**: Displays the calendar.
- **path('notifications/', Notifications.as_view(), name='notifications')**: Manages notifications.
- **path('notifications/create/', Notifications.as_view(), name='create_notification')**: Creates a new notification.
- **path('notifications/delete/<int:notification_id>/', DeleteNotification.as_view(), name='delete_notification')**: Deletes a specific notification.
- **path('tasks/', Tasks.as_view(), name='tasks')**: Displays tasks.
- **path('display_all_users/', Display_All_Users.as_view(), name='display_all_users')**: Lists all active users.
- **path('assign_user/', Assign_User.as_view(), name='assign_user')**: Assigns a user to a task or role.
- **path('create_section/', Create_Section.as_view(), name='create_section')**: Creates a new section.
- **path('edit_section/<str:sectionId>/', Edit_Section.as_view(), name='edit_section')**: Edits an existing section.
- **path('edit_course/<str:courseId>/', Edit_Course.as_view(), name='edit_course')**: Edits an existing course.
- **path('manage_courses_sections/', Manage_Courses_Sections.as_view(), name='manage_courses_sections')**: Manages courses and sections.
- **path('assignments/', ViewTAAssignments.as_view(), name="view_ta_assignments")**: Views TA assignments.
- **path('tasks/delete/<int:task_id>/', DeleteTask.as_view(), name='delete_task')**: Deletes a specific task.
- **path('edit_user_info/', EditUsers.as_view(), name='edit_user_info')**: Edits user information.
- **path('user_contact_card/', ContactCard.as_view(), name='contact_card')**: Displays the contact card for a user.
- **path('delete_user', Delete_User.as_view(), name='delete_user')**: Deletes a user.
- **path('send_email/', Email.as_view(), name='send_email')**: Sends an email.

#### 3. Inputs/Outputs/Side Effects
- **Inputs**: URL paths and parameters (e.g., `notification_id`, `task_id`).
- **Outputs**: Corresponding views rendering pages or performing actions.
- **Side Effects**: State changes in the application (e.g., user login, logout, creation of new entities).

#### 4. Design Patterns, Dependencies
- **Design Patterns**: Uses Django's class-based views for handling HTTP requests.
- **Dependencies**:
  - `django.contrib.admin`: Provides the admin interface.
  - `django.urls`: Handles URL routing.
  - Various views from `django_app.views` that handle specific functionalities.

#### 5. Cohesion and Coupling
- **Cohesion**: The file has high cohesion as it is dedicated to mapping URLs to their respective views, ensuring each path corresponds to a clear functionality.
- **Coupling**: Low coupling as each URL pattern is independent of others, except for the overarching Django framework that manages them.

This summary provides an overview of the project's URL configuration, detailing its purpose, key functionalities, and design aspects.