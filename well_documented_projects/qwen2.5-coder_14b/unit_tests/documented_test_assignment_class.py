```python
from django.test import TestCase, Client
from django.urls import reverse
from django_app.models import User, Course, Section, Assignment


class TasksViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create test users
        self.ta_user = User.objects.create(
            user_name="ta_user",
            password="password123",
            first_name="Test",
            last_name="TA",
            role_name="TA",
            email_address="ta@example.com",
            phone_number="123-456-7890",
            street_address="123 TA St",
            city="Milwaukee",
            state="WI",
            zip_code="12345"
        )

        self.instructor_user = User.objects.create(
            user_name="instructor_user",
            password="password123",
            first_name="Test",
            last_name="Instructor",
            role_name="Instructor",
            email_address="instructor@example.com",
            phone_number="123-456-7890",
            street_address="456 Instructor St",
            city="Madison",
            state="WI",
            zip_code="54321"
        )

        # Create course and section
        self.course = Course.objects.create(
            courseId="CS101",
            courseName="Intro to CS",
            credits=3,
            startDate="2024-01-01",
            endDate="2024-06-01"
        )

        self.section = Section.objects.create(
            course=self.course,
            sectionId="CS101-001",
            sectionType="LEC",
            sectionMeets="MWF 10:00-11:00",
            sectionLocation="Room 101"
        )

        # Create an assignment
        self.assignment = Assignment.objects.create(
            ta=self.ta_user,
            title="Grading Homework 1",
            description="Grade all submissions for Homework 1",
            due_date="2024-05-01",
            course=self.course,
            section=self.section
        )

        # Simulate a logged-in session
        session = self.client.session
        session['name'] = self.ta_user.user_name
        session.save()

    def test_get_tasks(self):
        """Test GET request for task listing."""
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks.html')
        self.assertContains(response, "Grading Homework 1")
        self.assertContains(response, "CS101")
        self.assertContains(response, "Test TA")

    def test_post_create_task(self):
        """Test POST request to create a new task."""
        response = self.client.post(reverse('tasks'), {
            'action': 'create',
            'task-name': 'New Task',
            'description': 'New Task Description',
            'due-date': '2024-06-01',
            'user_id': self.ta_user.user_name,
            'course_id': self.course.courseId,
            'section_id': self.section.sectionId
        })

        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertEqual(Assignment.objects.count(), 2)

        new_task = Assignment.objects.get(title="New Task")
        self.assertEqual(new_task.description, "New Task Description")
        self.assertEqual(new_task.ta, self.ta_user)
        self.assertEqual(new_task.course, self.course)
        self.assertEqual(new_task.section, self.section)

    def test_post_create_task_without_section(self):
        """Test creating a task without linking to a section."""
        response = self.client.post(reverse('tasks'), {
            'action': 'create',
            'task-name': 'Task Without Section',
            'description': 'Description Without Section',
            'due-date': '2024-06-01',
            'user_id': self.ta_user.user_name,
            'course_id': self.course.courseId,
            'section_id': ''  # No section
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Assignment.objects.count(), 2)

        task = Assignment.objects.get(title="Task Without Section")
        self.assertIsNone(task.section)

    def test_post_delete_task(self):
        """Test deleting a task."""
        response = self.client.post(reverse('delete_task', args=[self.assignment.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Assignment.objects.count(), 0)

    def test_mark_task_complete(self):
        """Test marking a task as complete."""
        response = self.client.post(reverse('tasks'), {
            'action': 'complete',
            'task_id': self.assignment.id
        })

        self.assertEqual(response.status_code, 302)
        self.assignment.refresh_from_db()
        self.assertTrue(self.assignment.completed)
```