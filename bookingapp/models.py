from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone

class Room(models.Model):

    ROOM_TYPES = [
        ('Deluxe', 'Deluxe Room'),
        ('Family', 'Family Room'),
        ('Suite', 'Luxury Suite'),
    ]

    name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price_per_night = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField(default=2)
    description = models.TextField()
    image = models.ImageField(upload_to='rooms/', blank=True, null=True)

    def is_available(self, check_in, check_out, exclude_booking_id=None):
        overlapping = Booking.objects.filter(
            room=self,
            check_in__lt=check_out,
            check_out__gt=check_in
        )

        if exclude_booking_id:
            overlapping = overlapping.exclude(id=exclude_booking_id)

        return not overlapping.exists()

    def get_booked_dates(self):
        return Booking.objects.filter(room=self).values(
            'check_in', 'check_out'
        )

    def __str__(self):
        return f"{self.name} - ₹{self.price_per_night}"


class Booking(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]

    status = models.CharField(
            max_length=20,
            choices=STATUS_CHOICES,
            default='Pending'
        )

    is_paid = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    email = models.EmailField()
    persons = models.PositiveIntegerField()

    check_in = models.DateField()
    check_out = models.DateField()

    total_price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_days(self):
        return (self.check_out - self.check_in).days

    def clean(self):

        if not self.room_id:
            return

        if self.check_in < timezone.now().date():
            raise ValidationError("Check-in cannot be in the past.")

        if self.check_out <= self.check_in:
            raise ValidationError("Check-out must be after check-in.")

        if self.persons > self.room.capacity:
            raise ValidationError(
                f"Room capacity exceeded. Max allowed: {self.room.capacity}"
            )

        if not self.room.is_available(
            self.check_in,
            self.check_out,
            exclude_booking_id=self.id
        ):
            raise ValidationError("Room not available for selected dates.")

    def save(self, *args, **kwargs):

        if self.room_id:
            self.full_clean()
            days = self.calculate_days()
            if days > 0:
                self.total_price = days * self.room.price_per_night

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.room.name}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
    
class GalleryImage(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='gallery/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else "Gallery Image"    