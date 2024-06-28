from django.db import models
from django.contrib.auth.models import User

class ParkingInfo(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    limit_number_car = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    price = models.CharField(max_length=100)
    start_time_work = models.CharField(max_length=20)
    end_time_work = models.CharField(max_length=20)
    features = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='products/')
    occupied_slots = models.PositiveIntegerField(null=True, blank=True, default=0)
    vacant_slots = models.PositiveIntegerField(null=True, blank=True, default=0)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




class Reservation(models.Model):
    ticket_code = models.CharField(max_length=6, blank=True, null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    finish_date = models.DateField()
    parking_zone = models.ForeignKey(ParkingInfo, on_delete=models.CASCADE)
    plate_number = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=16)
    checked_out = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'Reservation for vehicle: {self.plate_number}'