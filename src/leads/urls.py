from django.urls import path
from . import views

app_name = "leads"

urlpatterns = [
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path("privacy/", views.privacy, name="privacy"),
]
