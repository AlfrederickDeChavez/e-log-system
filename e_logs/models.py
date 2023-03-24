from django.db import models

# Create your models here.
class Bulletin(models.Model):
    author = models.CharField(max_length=200)
    priority = models.CharField(max_length=200)
    details = models.TextField()
    time = models.TimeField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.details

class Guest(models.Model):
    tower = models.CharField(max_length=200,null=True, blank=True)
    room = models.CharField(max_length=100, null=True, blank=True)
    affected_system = models.CharField(max_length=255, null=True, blank=True)
    attended_by = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time_reported = models.CharField(max_length=200, null=True, blank=True)
    time_resolved = models.CharField(max_length=200, null=True, blank=True)
    problem = models.TextField(null=True, blank=True)
    action = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=200, null=True, blank=True)
    recommendation = models.TextField(null=True, blank=True)
    time = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.tower + ' - ' + self.room + ' - ' + self.problem[0:20]


class Department(models.Model):
    department = models.CharField(max_length=200)
    client = models.CharField(max_length=100)
    affected_system = models.CharField(max_length=255)
    attended_by = models.CharField(max_length=200)
    date = models.DateField(null=True, blank=True)
    time_reported = models.CharField(max_length=100, null=True, blank=True)
    time_resolved = models.CharField(max_length=100, null=True, blank=True)
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
    t_lits = models.TimeField(null=True, blank=True)
    r_lits = models.CharField(max_length=500, null=True, blank=True)
    t_ciss = models.TimeField(null=True, blank=True)
    r_ciss = models.CharField(max_length=500, null=True, blank=True)
    t_cass = models.TimeField(null=True, blank=True)
    r_cass = models.CharField(max_length=500, null=True, blank=True)
    t_cebu = models.TimeField(null=True, blank=True)
    r_cebu = models.CharField(max_length=500, null=True, blank=True)
    t_boas = models.TimeField(null=True, blank=True)
    r_boas = models.CharField(max_length=500, null=True, blank=True)
    t_cwrge = models.TimeField(null=True, blank=True)
    r_cwrge = models.CharField(max_length=500, null=True, blank=True)
    t_utbeb = models.TimeField(null=True, blank=True)
    r_utbeb = models.CharField(max_length=500, null=True, blank=True)
    t_alicbu = models.TimeField(null=True, blank=True)
    r_alicbu = models.CharField(max_length=500, null=True, blank=True)
    t_ceu = models.TimeField(null=True, blank=True)
    r_ceu = models.CharField(max_length=500, null=True, blank=True)
    t_cdl = models.TimeField(null=True, blank=True)
    r_cdl = models.CharField(max_length=500, null=True, blank=True)
    t_cvti = models.TimeField( null=True, blank=True)
    r_cvti = models.CharField(max_length=500, null=True, blank=True)
    t_cppc = models.TimeField(null=True, blank=True)
    r_cppc = models.CharField(max_length=500, null=True, blank=True)
    t_ccrgt = models.TimeField(null=True, blank=True)
    r_ccrgt = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return 'Morning Shift' + ' - ' + str(self.date) + ' - ' + self.checked_by


class EveningTask(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    checked_by = models.CharField(max_length=200)
    t_dsob = models.TimeField(null=True, blank=True)
    r_dsob = models.CharField(max_length=500, null=True, blank=True)
    t_ceu = models.TimeField(null=True, blank=True)
    r_ceu = models.CharField(max_length=500, null=True, blank=True)
    t_cass = models.TimeField(null=True, blank=True)
    r_cass = models.CharField(max_length=500, null=True, blank=True)
    t_uebu = models.TimeField(null=True, blank=True)
    r_uebu = models.CharField(max_length=500, null=True, blank=True)
    t_alicbu = models.TimeField(null=True, blank=True)
    r_alicbu = models.CharField(max_length=500, null=True, blank=True)
    t_ciss = models.TimeField(null=True, blank=True)
    r_ciss = models.CharField(max_length=500, null=True, blank=True)
    t_cpss = models.TimeField(null=True, blank=True)
    r_cpss = models.CharField(max_length=500, null=True, blank=True)
    t_ccrgt = models.TimeField(null=True, blank=True)
    r_ccrgt = models.CharField(max_length=500, null=True, blank=True)
    t_cvti = models.TimeField(null=True, blank=True)
    r_cvti = models.CharField(max_length=500, null=True, blank=True)
    t_ltos = models.TimeField(null=True, blank=True)
    r_ltos = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return 'Evening Shift' + ' - ' + str(self.date) + ' - ' + self.checked_by


class Asset(models.Model):
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    supplier = models.CharField(max_length=200)
    purchase_date = models.DateField()
    expiration = models.DateField()
    schedule = models.CharField(max_length=150, null=True, blank=True)
    status = models.CharField(max_length=50)

    remarks = models.CharField(max_length=300, null=True, blank=True)
    current_tracking_date = models.DateField(null=True, blank=True)
    next_tracking_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name + " -- " + self.supplier

class Audit(models.Model):
    asset_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    supplier = models.CharField(max_length=200)
    purchase_date = models.DateField()
    schedule = models.CharField(max_length=150, null=True, blank=True)
    expiration = models.DateField()
    status = models.CharField(max_length=50, null=True, blank=True)

    remarks = models.CharField(max_length=300, null=True, blank=True)
    current_tracking_date = models.DateField(null=True, blank=True)
    next_tracking_date = models.DateField(null=True, blank=True)
    
    action = models.CharField(max_length=200)
    author = models.CharField(max_length=200, null=True, blank=True) 
    modified_date = models.DateField(auto_now_add=True, null=True, blank=True)
    modified_time = models.TimeField(auto_now_add=True, null=True, blank=True)
    modified_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.author} - {self.action} - {self.name}"


class RenewedAsset(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    supplier = models.CharField(max_length=200)
    purchase_date = models.DateField()
    expiration = models.DateField()
    schedule = models.CharField(max_length=150, null=True, blank=True)
    tracking_date = models.DateField(null=True, blank=True)
    remarks = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name + " -- " + self.supplier