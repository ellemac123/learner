from django.db import models

YEAR_IN_SCHOOL_CHOICES = (
    ('PK', 'Preschool'),
    ('K', 'Kindergarten'),
    ('1', 'First'),
    ('2', 'Second'),
    ('3', 'Third'),
    ('4', 'Fourth'),
    ('5', 'Fifth'),
    ('6', 'Sixth'),
    ('7', 'Seventh'),
    ('8', 'Eighth'),
    ('FR', 'Freshman'),
    ('SO', 'Sophomore'),
    ('JR', 'Junior'),
    ('SR', 'Senior'),
    ('GR', 'Graduate'),
)

TEACHER_PREFIX = (
    ('Miss', 'Miss'),
    ('Ms.', 'Ms.'),
    ('Mrs', 'Mrs.'),
    ('Mr.', 'Mr'),
    ('Dr.', 'Dr.')
)


class Student(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=50)

    student_year = models.CharField(choices=YEAR_IN_SCHOOL_CHOICES, default=YEAR_IN_SCHOOL_CHOICES[0], max_length=10)

    @property
    def full_name(self):
        """

        :return: a student's full name
        """

        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        return self.full_name


class Course(models.Model):
    course_name = models.CharField(max_length=50)
    course_description = models.TextField()

    students = models.ManyToManyField(Student, through='Enrollment')

    def __str__(self):
        return self.course_name


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    student_grade = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return '{} in course: {}'.format(self.student.last_name, self.course.course_name)


class Teacher(models.Model):
    prefix = models.CharField(choices=TEACHER_PREFIX, default=TEACHER_PREFIX[1], max_length=10)
    first_name = models.CharField("First Name", max_length=25)
    last_name = models.CharField("Last Name", max_length=50)

    @property
    def full_name(self):
        """

        :return: a teachers's full name
        """

        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        return self.full_name
