from django_app.models import CourseAssignment, Course, User, Section

class Assign:
    def __init__(self, post_data):
        """
        Initialize the Assign class with data from a POST request.

        :param post_data: A dictionary containing 'user', 'course', 'section', and 'grader_status' keys.
        """
        self.data = post_data
        self.user = post_data['user']
        self.course = post_data['course']
        self.section = post_data['section']
        self.grader_status = post_data['grader_status']

    def assign_user(self):
        """
        Assign a user to a course and section with the specified grader status.

        :return: The created CourseAssignment object.
        """
        # Fetch course, user, and section from the database using their IDs
        course = Course.objects.get(courseId=self.course)
        user = User.objects.get(user_name=self.user)
        section = Section.objects.get(sectionId=self.section)

        # Create a new CourseAssignment with fetched objects and provided grader status
        assignment = CourseAssignment.objects.create(
            course=course,
            user=user,
            section=section,
            role=self.grader_status
        )
        return assignment