from django.contrib import admin
from .models import Student, Course, Enrollment, Teacher


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'student_year')
    list_display = ('first_name', 'last_name', 'student_year')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    fields = ('course_name', 'course_description')
    list_display = ('course_name', 'course_description')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    fields = ('student', 'course', 'student_grade')
    list_display = ('student', 'course', 'student_grade')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    fields = ('prefix', 'first_name', 'last_name')
    list_display = ('last_name', 'first_name', 'prefix')
