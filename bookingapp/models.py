from django.db import models

# Create your models here.

from django.db import models

class Booking_table(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    t_persons = models.PositiveIntegerField()
    t_rooms = models.PositiveIntegerField()

    check_in = models.DateField()
    check_out = models.DateField()
    total_days = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def calculated_days(self):
        return (self.check_out - self.check_in).days

    def __str__(self):
        return f"{self.name} ({self.check_in} → {self.check_out})"

class Room(models.Model):
    ROOM_TYPES = [
        ('Deluxe', 'Deluxe Room'),
        ('Family', 'Family Room'),
        ('Suite', 'Luxury Suite'),
    ]

    name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price_per_night = models.PositiveIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='rooms/')

    def __str__(self):
        return f"{self.name} - ₹{self.price_per_night}"
    


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

