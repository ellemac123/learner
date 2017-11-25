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


class Student(models.Model):
    # student_id = models.CharField(max_length=20, primary_key=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=50)

    student_grade = models.CharField(choices=YEAR_IN_SCHOOL_CHOICES, max_length=1)

    @property
    def full_name(self):
        """

        :return: a student's full name
        """

        return '{} {}'.format(self.first_name, self.last_name)


class Course(models.Model):
    course_name = models.CharField(max_length=50)
    students = models.ManyToManyField(Student, through='Enrollment')
    # Many students in each course

    # def add_student_to_course(self):
    #


class Teacher(models.Model):
    first_name = models.CharField("First Name", max_length=25)
    last_name = models.CharField("Last Name", max_length=50)
    students = models.ManyToManyField(Student, through='Course')

    @property
    def full_name(self):
        """

        :return: a teachers's full name
        """

        return '{} {}'.format(self.first_name, self.last_name)


class Enrollment(models.Model):
    person = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
