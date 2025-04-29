```python
from datetime import date, datetime
from django_app.models import Course


class CreateCourse:
    def __init__(self, post_data):
        """
        Initialize the CreateCourse class with data from a POST request.

        :param post_data: Dictionary containing course details
        """
        self.data = post_data
        self.courseId = post_data['courseId']
        self.courseName = post_data['courseName']
        self.credits = post_data['credits']
        self.startDate = post_data['startDate']
        self.endDate = post_data['endDate']
        self.message = ''
        self.create_course()

    def wellFormed(self):
        """
        Check if the course data is well-formed and meets all validation criteria.

        :return: True if the data is well-formed, False otherwise
        """
        for key, value in self.data.items():
            if value is None or value.strip() == '':
                self.message = "Failed to Create Course: Missing Information"
                return False
        if not self.course_id_check(): 
            return False
        if not self.credit_check(): 
            return False
        if not self.date_check(): 
            return False
        return True


    def create_course(self):
        """
        Create a new course in the database if all validations pass.

        :return: The created Course object or False if validation fails
        """
        if not self.wellFormed(): 
            return False
        course = Course.objects.create(courseId=self.courseId,
                                         courseName=self.courseName,
                                        credits=self.credits,
                                        startDate=self.startDate,
                                        endDate=self.endDate
                                        )

        self.message = "Course Created Successfully"
        return course



    def date_check(self):
        """
        Validate that the start and end dates are valid.

        :return: True if dates are valid, False otherwise
        """
        date_start_date = datetime.strptime(self.startDate, '%Y-%m-%d').date()
        if date_start_date < date.today():
            self.message = "Start Date Cannot Be Earlier Than The Current Date"
            return False
        if self.endDate < self.startDate:
            self.message = "Start Date Cannot Be After The End Date"
            return False
        return True

    def is_two_digits(self):
        """
        Check if the credit value has more than two digits.

        :return: True if more than two digits, False otherwise
        """
        return len(self.credits) > 2

    def credit_check(self):
        """
        Validate that the credits are a whole number and within acceptable range.

        :return: True if credits are valid, False otherwise
        """
        if '.' in self.credits:
            self.message = "Credits Must Be A Whole Number"
            return False
        elif self.is_two_digits():
            self.message = "Credits Cannot Be More Than 2 Digits"
            return False
        elif int(self.credits) <= 0:
            self.message = "Credits Must Be Greater Than Zero"
            return False
        return True

    def course_id_check(self):
        """
        Validate that the course ID is unique and does not exceed 8 characters.

        :return: True if course ID is valid, False otherwise
        """
        length = len(self.courseId)
        if length > 8:
            self.message = "Course ID Cannot Be More Than 8 Characters"
            return False
        elif Course.objects.filter(courseId=self.courseId).exists():
            self.message = f"Course ID {self.courseId} Already Exists"
            return False
        elif Course.objects.filter(courseName=self.courseName).exists():
            self.message = f"Course Name {self.courseName} Already Exists"
            return False
        return True
```