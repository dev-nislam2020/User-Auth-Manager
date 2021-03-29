from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    BLOOD_GROUP = (
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    )
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    MARITAL_STATUS = (
        ('Unmarried', 'Unmarried'),
        ('Married', 'Married'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dob = models.DateField(blank=True, null=True)
    blood_group	= models.CharField(max_length=3, choices=BLOOD_GROUP)
    nationality	= models.CharField(max_length=50, blank=True, null=True)
    gender	= models.CharField(max_length=6, choices=GENDER)
    marital_status = models.CharField(max_length=9, choices=MARITAL_STATUS)

