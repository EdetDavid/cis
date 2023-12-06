# cases/models.py
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Criminal(models.Model):
    firstname = models.CharField(max_length=225)
    lastname = models.CharField(max_length=225)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='criminal_images/',
                              null=True, blank=True, default='default.png')

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class CriminalCase(models.Model):
    case_number = models.CharField(max_length=20)
    individual = models.ForeignKey(Criminal, on_delete=models.CASCADE)
    description = models.TextField()
    date_reported = models.DateTimeField(auto_now_add=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=1000)
    # Add more fields as needed

    def __str__(self):
        return f"Case #{self.case_number}"
