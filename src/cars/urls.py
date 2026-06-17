from django.urls import path

from . import views

app_name = "cars"

urlpatterns = [
    path("new/", views.new_cars_list, name="new_list"),
    path("used/", views.used_cars_list, name="used_list"),
    path("<int:pk>/", views.car_detail, name="car_detail"),
]
