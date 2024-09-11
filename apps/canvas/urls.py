from django.urls import path
from .views import PixelListAPIView, PixelPaintAPIView


urlpatterns = [
    path("pixels/", PixelListAPIView.as_view(), name="pixel-list"),
    path("paint/", PixelPaintAPIView.as_view(), name="pixel-paint"),
]
