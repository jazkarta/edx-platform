from django.db import models

from xmodule_django.models import CourseKeyField, LocationKeyField


class PersonalOnlineCourse(models.Model):
    """
    A Personal Online Course.
    """
    course_id = CourseKeyField(max_length=255, db_index=True)
    display_name = models.CharField(max_length=255)


class PersonalOnlineCourseFieldOverride(models.Model):
    """
    Field overrides for personal online courses.
    """
    poc = models.ForeignKey(PersonalOnlineCourse, db_index=True)
    location = LocationKeyField(max_length=255, db_index=True)

    class Meta:
        unique_together = (('poc', 'location', 'student'),)

    field = models.CharField(max_length=255)
    value = models.TextField(default='null')
