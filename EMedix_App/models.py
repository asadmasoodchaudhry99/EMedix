from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields import BooleanField
# Create your models here.


class userinfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=100)
    otp = models.IntegerField(default=0)
    otp_status = models.BooleanField(default=False)
    info_filled = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username


class patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=100, default='')
    age = models.IntegerField(default=0)
    country = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=100, default='')
    booking_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
        
class doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=100, default='')
    age = models.IntegerField(default=0)
    qualification = models.CharField(max_length=100, default='')
    department = models.CharField(max_length=100, default='')
    consultationcharges = models.IntegerField(default=0)
    country = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=100, default='')
    booking_count = models.IntegerField(default=0)
    

    def __str__(self):
        return self.user.username


class clinic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=100, default='')
    registration_number = models.CharField(max_length= 100, default='')
    country = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=100, default='')
    doctors = models.ManyToManyField(doctor)
    

    def __str__(self):
        return self.user.username

class BookingAppointment(models.Model):
    patient = models.ForeignKey(patient, on_delete= models.CASCADE)
    doctor = models.ForeignKey(doctor, on_delete=models.CASCADE)
    timing = models.DateTimeField()
    bookingtype = models.CharField(max_length=100, default='')
    explaination = models.TextField(max_length=2000, default='')
    prescription = models.TextField(max_length=2000,default='')
    prescription_status = models.BooleanField(default=False)
    consultation_status = models.BooleanField(default=False)
    def __str__(self):
        return self.patient.user.get_full_name() + " booked " + self.doctor.user.get_full_name()

class medical_records(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    desc = models.TextField()
    date = models.DateField(auto_now_add=True)
    upfile = models.FileField()

    def __str__(self):
        return self.user.username