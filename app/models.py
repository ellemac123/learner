from django.db import models

YEAR_IN_SCHOOL_CHOICES = (
    ('PK', 'Preschool'),
    ('K', 'Kindergarten'),
    ('1', 'First'),
    ('2', 'Second'),
    ('3', 'Third'),
    ('4', 'Third'),
    ('5', 'Third'),
    ('6', 'Third'),
    ('7', 'Third'),
    ('8', 'Third'),
    ('FR', 'Freshman'),
    ('SO', 'Sophomore'),
    ('JR', 'Junior'),
    ('SR', 'Senior'),
    ('GR', 'Graduate'),
)


class Teacher(models.Model):
    first_name = models.CharField("First Name", max_length=25)
    last_name = models.CharField("Last Name", max_length=50)


class Course(models.Model):
    course_name = models.CharField(max_length=50)
    instructor = models.OneToOneField(Teacher, related_name="courses")


class Student(models.Model):
    # student_id = models.CharField(max_length=20, primary_key=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=50)

    # student_grade =
