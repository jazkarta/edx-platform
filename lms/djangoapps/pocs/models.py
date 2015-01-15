from django.contrib.auth.models import User
from django.db import models

from xmodule_django.models import CourseKeyField, LocationKeyField


class PersonalOnlineCourse(models.Model):
    """
    A Personal Online Course.
    """
    course_id = CourseKeyField(max_length=255, db_index=True)
    display_name = models.CharField(max_length=255)
    coach = models.ForeignKey(User, db_index=True)


class PocMembership(models.Model):
    """
    Which students are in a POC?
    """
    poc = models.ForeignKey(PersonalOnlineCourse, db_index=True)
    student = models.ForeignKey(User, db_index=True)


class PocFieldOverride(models.Model):
    """
    Field overrides for personal online courses.
    """
    poc = models.ForeignKey(PersonalOnlineCourse, db_index=True)
    location = LocationKeyField(max_length=255, db_index=True)

    class Meta:
        unique_together = (('poc', 'location', 'student'),)

    field = models.CharField(max_length=255)
    value = models.TextField(default='null')
