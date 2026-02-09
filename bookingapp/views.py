from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Booking_table
from datetime import datetime
from .models import ContactMessage
from .models import Room


# ---------------- HOME ----------------
def index_view(request):
    return render(request, 'bookingapp/index.html')


# ---------------- CREATE BOOKING ----------------
def create_view(request):
    if request.method == 'POST':
        check_in_str = request.POST.get('check_in')
        check_out_str = request.POST.get('check_out')

        # 🔒 Safety check
        if not check_in_str or not check_out_str:
            messages.error(request, "Please select check-in and check-out dates.")
            return redirect('/create_booking/')

        check_in = datetime.strptime(check_in_str, "%Y-%m-%d").date()
        check_out = datetime.strptime(check_out_str, "%Y-%m-%d").date()

        total_days = (check_out - check_in).days

        if total_days <= 0:
            messages.error(request, "Check-out date must be after check-in date.")
            return redirect('/create_booking/')

        Booking_table.objects.create(
            name=request.POST.get('f_name'),
            email=request.POST.get('Email'),
            t_persons=request.POST.get('No_of_Person'),
            t_rooms=request.POST.get('No_of_Rooms'),
            check_in=check_in,
            check_out=check_out,
            total_days=total_days, 
        )

        messages.success(request, f"Booking confirmed for {total_days} days!")
        return redirect('/display_booking/')

    return render(request, 'bookingapp/create.html')


# ---------------- ROOMS ----------------
def rooms_view(request):
    rooms = Room.objects.all()
    return render(request, 'bookingapp/rooms.html', {'rooms': rooms})


# ---------------- DISPLAY BOOKINGS ----------------
def display_view(request):
    data = Booking_table.objects.all()
    return render(request, 'bookingapp/display.html', {'data': data})


# ---------------- UPDATE BOOKING ----------------
def update_booking(request, id):
    booking = get_object_or_404(Booking_table, id=id)

    if request.method == 'POST':
        booking.name = request.POST.get('f_name')
        booking.email = request.POST.get('Email')
        booking.t_persons = request.POST.get('No_of_Person')
        booking.t_rooms = request.POST.get('No_of_Rooms')

        check_in = datetime.strptime(request.POST.get('check_in'), "%Y-%m-%d").date()
        check_out = datetime.strptime(request.POST.get('check_out'), "%Y-%m-%d").date()

        booking.check_in = check_in
        booking.check_out = check_out
        booking.total_days = (check_out - check_in).days

        booking.save()
        messages.success(request, "Booking updated successfully!")
        return redirect('/display_booking/')

    return render(request, 'bookingapp/update.html', {'booking': booking})


# ---------------- DELETE BOOKING ----------------
def delete_booking(request, id):
    booking = get_object_or_404(Booking_table, id=id)

    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Booking deleted successfully!")
        return redirect('/display_booking/')

    return render(request, 'bookingapp/delete.html', {'booking': booking})

def gallery_view(request):
    return render(request, 'bookingapp/gallery.html')

def about_view(request):
    return render(request, 'bookingapp/about.html')

def contact_view(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            message=request.POST.get('message')
        )
        return redirect('thank_you')

    return render(request, 'bookingapp/contact.html')

def thank_you(request):
    return render(request, 'bookingapp/thank_you.html')