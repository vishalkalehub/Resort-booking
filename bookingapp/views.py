from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from .models import Room, Booking, ContactMessage, GalleryImage
from .forms import BookingForm
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from django.contrib.auth.views import LoginView
from .forms import LoginForm
from django.core.exceptions import ValidationError
# -----------------------------
# HTML VIEWS
# -----------------------------

def index_view(request):
    return render(request, 'bookingapp/index.html')

def rooms_view(request):
    rooms = Room.objects.all()

    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')

    if check_in and check_out:
        try:
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()

            available_rooms = []

            for room in rooms:
                if room.is_available(check_in_date, check_out_date):
                    available_rooms.append(room.id)

            rooms = Room.objects.filter(id__in=available_rooms)

        except ValueError:
            pass  # if invalid date format

    return render(request, 'bookingapp/rooms.html', {'rooms': rooms})


@login_required
def room_detail_view(request, id):
    room = get_object_or_404(Room, id=id)

    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.user = request.user

            try:
                booking.save()
                messages.success(request, "🎉 Booking confirmed successfully!")
                return redirect("index")

            except ValidationError as e:
                # Attach error to form properly
                for error in e.messages:
                    form.add_error(None, error)

        else:
            print("FORM ERRORS:", form.errors)

    else:
        form = BookingForm()

    return render(request, "bookingapp/room_detail.html", {
        "room": room,
        "form": form
    })

def gallery_view(request):
    images = GalleryImage.objects.all().order_by('-created_at')
    return render(request, 'bookingapp/gallery.html', {'images': images})

def create_view(request):

    form = BookingForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Booking confirmed successfully!")
            return redirect("display_booking")
        else:
            print("FORM ERRORS:", form.errors)  # 🔥 ADD THIS

    return render(request, "bookingapp/create.html", {"form": form})

def check_availability(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')

    if not check_in or not check_out:
        return JsonResponse({"error": "Dates required"}, status=400)

    check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
    check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()

    available = room.is_available(check_in_date, check_out_date)

    if available:
        return JsonResponse({"available": True})
    else:
        return JsonResponse({
            "available": False,
            "booked_dates": list(room.get_booked_dates())
        })
    
@login_required
def display_view(request):
    data = Booking.objects.all()
    return render(request, 'bookingapp/display.html', {'data': data})


def update_booking(request, id):
    booking = get_object_or_404(Booking, id=id)

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking updated successfully!")
            return redirect('display_booking')
    else:
        form = BookingForm(instance=booking)

    return render(request, 'bookingapp/update.html', {'form': form})


def delete_booking(request, id):
    booking = get_object_or_404(Booking, id=id)

    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Booking deleted!")
        return redirect('display_booking')

    return render(request, 'bookingapp/delete.html', {'booking': booking})


def contact_view(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            message=request.POST.get('message')
        )
        return redirect('thank_you')

    return render(request, 'bookingapp/contact.html')


def about_view(request):
    return render(request, 'bookingapp/about.html')


def thank_you(request):
    return render(request, 'bookingapp/thank_you.html')


def admin_only(user):
    return user.is_superuser


@user_passes_test(admin_only)
def dashboard_view(request):
    total_revenue = Booking.objects.aggregate(
        Sum('total_price')
    )['total_price__sum'] or 0

    context = {
        'total_bookings': Booking.objects.count(),
        'total_revenue': total_revenue,
        'total_rooms': Room.objects.count(),
        'total_contacts': ContactMessage.objects.count(),
    }

    return render(request, 'bookingapp/dashboard.html', context)


# -----------------------------
# API VIEWSETS
# -----------------------------

from rest_framework import viewsets, permissions
from .serializers import RoomSerializer, BookingSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny]


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)   # ✅ Auto login after register
            return redirect('/')   # Redirect to home
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})       

class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = LoginForm

    def form_valid(self, form):
        messages.success(self.request, "Login successful! Welcome back.")
        return super().form_valid(form)