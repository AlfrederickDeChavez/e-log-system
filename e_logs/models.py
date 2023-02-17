from django.db import models

# Create your models here.
class Bulletin(models.Model):
    author = models.CharField(max_length=200)
    priority = models.CharField(max_length=200)
    details = models.TextField()
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.details


class Guest(models.Model):
    tower = models.CharField(max_length=200)
    room = models.CharField(max_length=100)
    affected_system = models.CharField(max_length=255)
    attended_by = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    time_reported = models.TimeField()
    time_resolved = models.TimeField()
    problem = models.TextField()
    action = models.TextField()
    status = models.CharField(max_length=200)
    recommendation = models.TextField()

    def __str__(self):
        return self.tower + ' - ' + self.room + ' - ' + self.problem[0:20]



class Department(models.Model):
    department = models.CharField(max_length=200)
    client = models.CharField(max_length=100)
    affected_system = models.CharField(max_length=255)
    attended_by = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    time_reported = models.TimeField()
    time_resolved = models.TimeField()
    problem = models.TextField()
    action = models.TextField()
    status = models.CharField(max_length=200)
    recommendation = models.TextField()

    def __str__(self):
        return self.department + ' - ' + self.problem[0:20]