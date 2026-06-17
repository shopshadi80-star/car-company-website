from django.shortcuts import render
from .models import Car


def home(request):
    latest_used = (
        Car.objects.filter(car_type=Car.CarType.USED, status=Car.Status.AVAILABLE)
        .prefetch_related("images")
        .order_by("-created_at")[:6]
    )
    latest_new = (
        Car.objects.filter(car_type=Car.CarType.NEW, status=Car.Status.AVAILABLE)
        .prefetch_related("images")
        .order_by("-created_at")[:3]
    )
    return render(request, "home.html", {
        "latest_used": latest_used,
        "latest_new": latest_new,
    })
