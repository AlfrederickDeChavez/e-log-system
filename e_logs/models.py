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

class MorningTask(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    checked_by = models.CharField(max_length=200)
    t_lits = models.TimeField()
    r_lits = models.CharField(max_length=500)
    t_ciss = models.TimeField()
    r_ciss = models.CharField(max_length=500)
    t_cass = models.TimeField()
    r_cass = models.CharField(max_length=500)
    t_cebu = models.TimeField()
    r_cebu = models.CharField(max_length=500)
    t_boas = models.TimeField()
    r_boas = models.CharField(max_length=500)
    t_cwrge = models.TimeField()
    r_cwrge = models.CharField(max_length=500)
    t_utbeb = models.TimeField()
    r_utbeb = models.CharField(max_length=500)
    t_alicbu = models.TimeField()
    r_alicbu = models.CharField(max_length=500)
    t_ceu = models.TimeField()
    r_ceu = models.CharField(max_length=500)
    t_cdl = models.TimeField()
    r_cdl = models.CharField(max_length=500)
    t_cvti = models.TimeField()
    r_cvti = models.CharField(max_length=500)
    t_cppc = models.TimeField()
    r_cppc = models.CharField(max_length=500)
    t_ccrgt = models.TimeField()
    r_ccrgt = models.CharField(max_length=500)

    def __str__(self):
        return 'Morning Shift' + ' - ' + str(self.date) + ' - ' + self.checked_by


class EveningTask(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    checked_by = models.CharField(max_length=200)
    t_dsob = models.TimeField()
    r_dsob = models.CharField(max_length=500)
    t_ceu = models.TimeField()
    r_ceu = models.CharField(max_length=500)
    t_cass = models.TimeField()
    r_cass = models.CharField(max_length=500)
    t_uebu = models.TimeField()
    r_uebu = models.CharField(max_length=500)
    t_alicbu = models.TimeField()
    r_alicbu = models.CharField(max_length=500)
    t_ciss = models.TimeField()
    r_ciss = models.CharField(max_length=500)
    t_cpss = models.TimeField()
    r_cpss = models.CharField(max_length=500)
    t_ccrgt = models.TimeField()
    r_ccrgt = models.CharField(max_length=500)
    t_cvti = models.TimeField()
    r_cvti = models.CharField(max_length=500)
    t_ltos = models.TimeField()
    r_ltos = models.CharField(max_length=500)

    def __str__(self):
        return 'Evening Shift' + ' - ' + str(self.date) + ' - ' + self.checked_by