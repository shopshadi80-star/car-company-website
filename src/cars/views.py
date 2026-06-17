from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Car, Brand
from leads.forms import TestDriveForm, InspectionForm


def home(request):
    latest_used = Car.objects.filter(car_type=Car.CarType.USED, status=Car.Status.AVAILABLE).select_related("brand").prefetch_related("images")[:6]
    latest_new = Car.objects.filter(car_type=Car.CarType.NEW, status=Car.Status.AVAILABLE).select_related("brand").prefetch_related("images")[:3]
    return render(request, "home.html", {"latest_used": latest_used, "latest_new": latest_new})


def new_cars_list(request):
    cars = Car.objects.filter(car_type=Car.CarType.NEW, status=Car.Status.AVAILABLE).select_related("brand").prefetch_related("images")

    brands = Brand.objects.filter(car__car_type=Car.CarType.NEW, car__status=Car.Status.AVAILABLE).distinct()
    years = Car.objects.filter(car_type=Car.CarType.NEW, status=Car.Status.AVAILABLE).values_list("year", flat=True).order_by("-year").distinct()

    brand_id = request.GET.get("brand")
    year = request.GET.get("year")
    price_min = request.GET.get("price_min")
    price_max = request.GET.get("price_max")

    if brand_id:
        cars = cars.filter(brand_id=brand_id)
    if year:
        cars = cars.filter(year=year)
    if price_min:
        cars = cars.filter(price__gte=price_min)
    if price_max:
        cars = cars.filter(price__lte=price_max)

    context = {
        "cars": cars,
        "brands": brands,
        "years": years,
        "selected_brand": brand_id,
        "selected_year": year,
        "price_min": price_min,
        "price_max": price_max,
    }
    return render(request, "cars/new_cars_list.html", context)


def used_cars_list(request):
    cars = Car.objects.filter(car_type=Car.CarType.USED, status=Car.Status.AVAILABLE).select_related("brand").prefetch_related("images")

    brands = Brand.objects.filter(car__car_type=Car.CarType.USED, car__status=Car.Status.AVAILABLE).distinct()
    cities = Car.objects.filter(car_type=Car.CarType.USED, status=Car.Status.AVAILABLE).exclude(city="").values_list("city", flat=True).order_by("city").distinct()
    years = Car.objects.filter(car_type=Car.CarType.USED, status=Car.Status.AVAILABLE).values_list("year", flat=True).order_by("-year").distinct()

    brand_id = request.GET.get("brand")
    year = request.GET.get("year")
    city = request.GET.get("city")
    price_min = request.GET.get("price_min")
    price_max = request.GET.get("price_max")

    if brand_id:
        cars = cars.filter(brand_id=brand_id)
    if year:
        cars = cars.filter(year=year)
    if city:
        cars = cars.filter(city=city)
    if price_min:
        cars = cars.filter(price__gte=price_min)
    if price_max:
        cars = cars.filter(price__lte=price_max)

    context = {
        "cars": cars,
        "brands": brands,
        "cities": cities,
        "years": years,
        "selected_brand": brand_id,
        "selected_year": year,
        "selected_city": city,
        "price_min": price_min,
        "price_max": price_max,
    }
    return render(request, "cars/used_cars_list.html", context)


def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk, status=Car.Status.AVAILABLE)
    images = car.images.all()

    if car.car_type == Car.CarType.NEW:
        form_class = TestDriveForm
        form_submitted_key = "test_drive_sent"
    else:
        form_class = InspectionForm
        form_submitted_key = "inspection_sent"

    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.car = car
            obj.save()
            messages.success(request, "تم إرسال طلبك بنجاح، سنتواصل معك قريباً.")
            return redirect("cars:car_detail", pk=pk)
    else:
        form = form_class()

    context = {
        "car": car,
        "images": images,
        "form": form,
    }
    return render(request, "cars/car_detail.html", context)