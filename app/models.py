from django.db import models


class Teacher(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=50)
