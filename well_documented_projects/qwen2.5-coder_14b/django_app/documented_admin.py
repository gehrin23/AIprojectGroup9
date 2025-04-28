```python
from django.contrib import admin
from django_app import models


# Register your models here.
class userAdmin(admin.ModelAdmin):
    # Define the fields to be displayed in the admin panel for User model
    list_display = ('user_name', 'first_name', 'last_name', 'street_address', 'state', 'zip_code', 'role_name', 'date_created')


class courseAdmin(admin.ModelAdmin):
    # Define the fields to be displayed in the admin panel for Course model
    list_display = ('courseName', 'courseId', 'credits')


class sectionAdmin(admin.ModelAdmin):
    # Define the fields to be displayed in the admin panel for Section model
    list_display = ('course', 'sectionId', 'sectionType')



admin.site.register(models.User, userAdmin)
admin.site.register(models.Course, courseAdmin)
admin.site.register(models.Section, sectionAdmin)
```

**Onboarding PDF Summary**

1. **Overall File Purpose:**
   - This file is part of a Django application and is responsible for registering models with the Django admin site to provide an interface for managing data.

2. **Key Functions/Methods and Their Responsibilities:**
   - `userAdmin`: Inherits from `admin.ModelAdmin` and specifies which fields of the User model should be displayed in the admin panel.
   - `courseAdmin`: Inherits from `admin.ModelAdmin` and specifies which fields of the Course model should be displayed in the admin panel.
   - `sectionAdmin`: Inherits from `admin.ModelAdmin` and specifies which fields of the Section model should be displayed in the admin panel.

3. **Inputs/Outputs/Side Effects:**
   - **Inputs:** The models `User`, `Course`, and `Section` from the `django_app.models` module.
   - **Outputs:** Registers these models with the Django admin site, making them accessible via the admin interface.
   - **Side Effects:** None.

4. **Design Patterns, Dependencies:**
   - **Design Patterns:** This code follows the Django admin customization pattern by extending `admin.ModelAdmin`.
   - **Dependencies:** 
     - `django.contrib.admin` for the admin site functionality.
     - `django_app.models` for accessing the defined models.

5. **Point Out Cohesion and Coupling:**
   - **Cohesion:** High cohesion within each class (`userAdmin`, `courseAdmin`, `sectionAdmin`) as they are focused on customizing the display of specific models in the admin panel.
   - **Coupling:** Low coupling between classes, as each is responsible for a different model and does not interact with others directly.