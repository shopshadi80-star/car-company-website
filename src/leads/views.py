from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ContactForm


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تم إرسال رسالتك بنجاح، سنتواصل معك قريباً.")
            return redirect("leads:contact")
    else:
        form = ContactForm()

    return render(request, "leads/contact.html", {"form": form})
