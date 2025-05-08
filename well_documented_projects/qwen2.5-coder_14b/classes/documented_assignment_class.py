from django_app.models import User, Assignment

class AssignmentHandler:
    def __init__(self):
        """
        Initializes a new instance of the AssignmentHandler class.

        :param self.ta_assignments: A dictionary to store TA assignments.
        """
        self.ta_assignments = {}

    def get_all_ta_assignments(self):
        """
        :return: A dictionary containing Teaching Assistants as keys and their assigned tasks as values.
        """
        tas = User.objects.filter(role_name="TA").prefetch_related("assignments")
        self.ta_assignments = {ta: ta.assignments.all() for ta in tas}
        return self.ta_assignments
