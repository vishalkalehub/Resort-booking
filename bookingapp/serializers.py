from rest_framework import serializers
from .models import Room, Booking


# -----------------------------
# ROOM SERIALIZER
# -----------------------------
class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'


# -----------------------------
# BOOKING SERIALIZER
# -----------------------------
class BookingSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    total_price = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['is_paid', 'created_at']