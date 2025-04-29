from django.core.exceptions import ValidationError
from django.http import QueryDict
from django_app.models import Section, Course

class SectionClass:
    # Multi-function constructor checks if the input is a QueryDict else assumes it's a sectionId
    def __init__(self, post_data):

        if isinstance(post_data, QueryDict):
            self.fullId = ''
            if 'course' not in post_data:
                self.course = None
            else:
                self.course = Course.objects.get(courseId=post_data['course'])
                self.fullId += self.course.courseId
            self.sectionId = post_data['sectionId']
            self.fullId += ('-' + self.sectionId)
            self.sectionType = post_data['sectionType']
            self.sectionMeets = post_data['sectionMeets']
            self.sectionLocation = post_data['sectionLocation']

        else:
            try:
                self.section = Section.objects.get(sectionId=post_data)
                self.fullId = self.section.sectionId
                l = self.fullId.split('-')
                self.course = l[0]
                self.sectionId = l[1]
                self.sectionType = self.section.sectionType
                self.sectionMeets = self.section.sectionMeets
                self.sectionLocation = self.section.sectionLocation
            except Section.DoesNotExist:
                raise ValidationError('Section does not exist')

    # This method actually creates the section and returns if created and a message for successful creation or error
    def createSection(self):
        wellDone = self.wellFormed()
        if wellDone[0]:
            sect = Section.objects.create(course=self.course,
                                          sectionId=self.fullId,
                                          sectionType=self.sectionType,
                                          sectionMeets=self.sectionMeets,
                                          sectionLocation=self.sectionLocation,
                                          )
            sect.save()
            self.section = sect
        return wellDone

    def editSection(self, post_data):
        # Validate and update the section with new data
        message = self.editFormation(post_data)
        if message[0]:
            self.section.sectionType = post_data['sectionType']
            self.section.sectionMeets = post_data['sectionMeets']
            self.section.sectionLocation = post_data['sectionLocation']
            self.section.save()
        return message

    def editFormation(self, post_data):
        # Check for validation errors in the section data
        def editError(message):
            return False, message

        if len(post_data['sectionMeets']) > 32:
            return editError('Meeting days must be less than 33 characters')
        if len(post_data['sectionLocation']) > 128:
            return editError('Location must be less than 129 characters')
        return True, 'Section' + self.fullId + 'updated successfully'

    # Just delete section
    def deleteSection(self):
        self.section.delete()

    # Check if the section has the correct field lengths and the section is unique
    def wellFormed(self):
        if self.checkCourse():
            return False, 'There must be a course to assign to'
        if self.checkUniq():
            return False, 'There is already a section with this id'
        if self.checkId():
            return False, 'Id must be filled and less than 9 characters'
        if self.checkMeets():
            return False, 'Meeting days must be less than 33 characters'
        if self.checkLocation():
            return False, 'Location must be less than 129 characters'
        return True, 'Section was created successfully'

    # Methods for checking attributes of the section return true if in violation
    def checkUniq(self):
        return Section.objects.filter(sectionId=self.fullId).exists()

    def checkCourse(self):
        return self.course is None

    def checkId(self):
        l = len(self.sectionId)
        return l > 8 or l < 1

    def checkMeets(self):
        return len(self.sectionMeets) > 32

    def checkLocation(self):
        return len(self.sectionLocation) > 128