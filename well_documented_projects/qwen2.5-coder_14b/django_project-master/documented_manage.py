```python
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys

def main():
    """Run administrative tasks."""
    # Set the default settings module for the 'django_project' project
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
    
    try:
        # Import the execute_from_command_line function from Django's core management module
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Raise an informative error message if Django is not installed or available
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Execute the command-line utility with the arguments passed to the script
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    # Call the main function if this script is executed as the main module
    main()
```

### Onboarding PDF Summary

1. **Overall File Purpose:**
   - This Python script serves as the entry point for running administrative tasks in a Django project named `django_project`. It sets up the necessary environment and executes Django's command-line utility.

2. **Key Functions/Methods and Their Responsibilities:**
   - `main()`: The primary function responsible for running administrative tasks.
     - Sets the default settings module for the Django project.
     - Attempts to import `execute_from_command_line` from Django's core management module.
     - Raises an informative error if Django is not installed or available.
     - Executes the command-line utility with the arguments passed to the script.

3. **Inputs/Outputs/Side Effects:**
   - **Inputs:** 
     - The script takes command-line arguments (`sys.argv`), which are forwarded to Django's command-line utility.
   - **Outputs:**
     - Depends on the specific Django administrative task executed (e.g., running a server, managing database migrations).
   - **Side Effects:**
     - Initializes the Django environment with the specified settings module.
     - Executes various administrative tasks based on the provided command-line arguments.

4. **Design Patterns and Dependencies:**
   - **Design Pattern:** 
     - The script follows a standard entry-point pattern for Python scripts, using `if __name__ == '__main__':` to ensure that the `main()` function is only called when the script is executed directly.
   - **Dependencies:**
     - The script depends on Django being installed and available in the Python environment.

5. **Cohesion and Coupling:**
   - **Cohesion:** 
     - High cohesion within the `main()` function, as all lines of code are closely related to setting up and running the Django administrative tasks.
   - **Coupling:**
     - Low coupling with external systems or modules, focusing solely on interacting with Django's command-line utilities.

This script is essential for managing various aspects of a Django project through command-line interfaces.