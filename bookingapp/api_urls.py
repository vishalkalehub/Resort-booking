from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, BookingViewSet

router = DefaultRouter()
router.register('rooms', RoomViewSet)
router.register('bookings', BookingViewSet, basename='booking')

urlpatterns = router.urls