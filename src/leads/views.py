from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse

from .forms import ContactForm


def contact(request):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            if is_ajax:
                return JsonResponse({"success": True, "message": "تم إرسال رسالتك بنجاح، سنتواصل معك قريباً."})
            messages.success(request, "تم إرسال رسالتك بنجاح، سنتواصل معك قريباً.")
            return redirect("leads:contact")
        else:
            if is_ajax:
                errors = {field: list(errs) for field, errs in form.errors.items()}
                return JsonResponse({"success": False, "errors": errors}, status=400)
    else:
        form = ContactForm()

    return render(request, "leads/contact.html", {"form": form})
