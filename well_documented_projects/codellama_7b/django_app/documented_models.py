Here is the revised code with inline comments and docstrings added:
```python
from datetime import datetime
from django.core.validators import MinLengthValidator
from django.db import models

class User(models.Model):
    """A user in the system."""
    
    class Role(models.TextChoices):
        """Roles of users in the system.
        
        Teachers_Assistant: A teacher's assistant.
        Instructor: An instructor.
        Admin_Supervisor: An administrator or supervisor.
        """
    
    class USState(models.TextChoices):
        """States in the United States."""
        
        AL = 'AL'
        AK = 'AK'
        AZ = 'AZ'
        AR = 'AR'
        CA = 'CA'
        CO = 'CO'
        CT = 'CT'
        DE = 'DE'
        FL = 'FL'
        GA = 'GA'
        HI = 'HI'
        ID = 'ID'
        IL = 'IL'
        IN = 'IN'
        IA = 'IA'
        KS = 'KS'
        KY = 'KY'
        LA = 'LA'
        ME = 'ME'
        MD = 'MD'
        MA = 'MA'
        MI = 'MI'
        MN = 'MN'
        MS = 'MS'
        MO = 'MO'
        MT = 'MT'
        NE = 'NE'
        NV = 'NV'
        NH = 'NH'
        NJ = 'NJ'
        NM = 'NM'
        NY = 'NY'
        NC = 'NC'
        ND = 'ND'
        OH = 'OH'
        OK = 'OK'
        OR = 'OR'
        PA = 'PA'
        RI = 'RI'
        SC = 'SC'
        SD = 'SD'
        TN = 'TN'
        TX = 'TX'
        UT = 'UT'
        VT = 'VT'
        VA = 'VA'
        WA = 'WA'
        WV = 'WV'
        WI = 'WI'
        WY = 'WY'
    
    user_name = models.CharField(unique=True, max_length=20, verbose_name="User Name", null=False, default=None,primary_key=True)
    """The unique name of the user."""
    
    password = models.CharField(max_length=20, validators=[MinLengthValidator(8)], verbose_name="Password", null=False,default=None)
    """The password for the user."""
    
    first_name = models.CharField(max_length=15, verbose_name="First Name", null=False, default=None)
    """The first name of the user."""
    
    last_name = models.CharField(max_length=15, verbose_name="Last Name", null=False, default=None)
    """The last name of the user."""
    
    email_address = models.EmailField(unique=True, verbose_name="Email Address", null=False, default=None)
    """The email address of the user."""
    
    street_address = models.CharField(max_length=250, verbose_name="Street Address", null =False, default=None)
    """The street address of the user."""
    
    city = models.CharField(max_length=250, verbose_name="City", null=False, default=None)
    """The city where the user lives."""
    
    state = models.CharField(max_length=2, verbose_name="Home State", choices=USState.choices, null=False, default=None)
    """The home state of the user."""
    
    zip_code = models.CharField(max_length=5, verbose_name="Zip Code", null=False, default=None)
    """The zip code where the user lives."""
    
    phone_number = models.CharField(max_length=12, verbose_name="Phone Number", null=False, default=None)
    """The phone number of the user."""
    
    role_name = models.CharField(verbose_name="Users Role Type", choices=Role.choices, max_length=16)
    """The role type of the user."""
    
    date_created = models.CharField(verbose_name="Date Created", max_length=10,default=datetime.now().strftime('%m/%d/%Y'))
    """The date when the user was created."""
    
    date_updated = models.CharField(verbose_name="Last Updated", max_length=10, default=datetime.now().strftime('%m/%d/%Y'))
    """The date when the user was last updated."""
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    """Returns a string representation of the user."""

class Course(models.Model):
    """A course in the system."""
    
    courseId = models.CharField(verbose_name="Course ID", max_length=8, primary_key=True)
    """The unique identifier for the course."""
    
    credits = models.DecimalField(verbose_name="Credits", max_digits=2, decimal_places=0)
    """The number of credits required to complete the course."""
    
    courseName = models.CharField(verbose_name="Course Name", max_length=64)
    """The name of the course."""
    
    startDate = models.CharField(verbose_name="Start Date", max_length=10)
    """The date when the course starts."""
    
    endDate = models.CharField(verbose_name="End Date", max_length=10)
    """The date when the course ends."""
    
    def __str__(self):
        return f"{self.courseName}"
    """Returns a string representation of the course."""

class Section(models.Model):
    """A section in the system."""
    
    course = models.ForeignKey(Course, related_name="Sections", on_delete=models.CASCADE)
    """The course that the section belongs to."""
    
    sectionId = models.CharField(verbose_name="Section", max_length=16, primary_key=True, null=False)
    """The unique identifier for the section."""
    
    sectionType = models.CharField(verbose_name="Type", max_length=4)
    """The type of section (e.g., lecture, lab)."""
    
    sectionMeets = models.CharField(verbose_name="Meets", max_length=32)
    """When the section meets."""
    
    sectionLocation = models.CharField(verbose_name="Location", max_length=128)
    """The location of the section."""
    
    instructors = models.ManyToManyField(User, blank=True)
    """The instructor who teaches the section."""
    
    def __str__(self):
        return f"{self.sectionId}"
    """Returns a string representation of the section."""

class Assignment(models.Model):
    """An assignment in the system."""
    
    ta = models.ForeignKey(User, related_name="assignments", on_delete=models.CASCADE)
    """The teacher's assistant who created the assignment."""
    
    title = models.CharField(max_length=100)
    """The title of the assignment."""
    
    description = models.TextField()
    """A description of the assignment."""
    
    due_date = models.DateField()
    """The due date for the assignment."""
    
    def __str__(self):
        return f"{self.title}"
    """Returns a string representation of the assignment."""

class CourseRegistration(models.Model):
    """A course registration in the system."""
    
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    """The student who registered for the course."""
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    """The course that the student registered for."""
    
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    """The section of the course that the student registered for."""
    
    date = models.DateField()
    """The date when the registration was made."""
    
    def __str__(self):
        return f"{self.student} - {self.course}"
    """Returns a string representation of the course registration."""
```