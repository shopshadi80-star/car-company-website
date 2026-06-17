from django import forms

from .models import TestDriveRequest, InspectionRequest, ContactMessage


class TestDriveForm(forms.ModelForm):
    class Meta:
        model = TestDriveRequest
        fields = ["name", "phone", "preferred_time", "note"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "الاسم الكامل"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "05XXXXXXXX"}),
            "preferred_time": forms.TextInput(attrs={"class": "form-control", "placeholder": "مثال: الأحد من 10 صباحاً إلى 2 ظهراً"}),
            "note": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "أي ملاحظة إضافية (اختياري)"}),
        }
        labels = {
            "name": "الاسم",
            "phone": "رقم الجوال",
            "preferred_time": "الوقت المفضل",
            "note": "ملاحظة",
        }


class InspectionForm(forms.ModelForm):
    class Meta:
        model = InspectionRequest
        fields = ["name", "phone", "preferred_time", "note"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "الاسم الكامل"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "05XXXXXXXX"}),
            "preferred_time": forms.TextInput(attrs={"class": "form-control", "placeholder": "مثال: الأحد من 10 صباحاً إلى 2 ظهراً"}),
            "note": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "أي ملاحظة إضافية (اختياري)"}),
        }
        labels = {
            "name": "الاسم",
            "phone": "رقم الجوال",
            "preferred_time": "الوقت المفضل",
            "note": "ملاحظة",
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "phone", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "الاسم الكامل"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "05XXXXXXXX"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "example@email.com"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "اكتب رسالتك هنا..."}),
        }
        labels = {
            "name": "الاسم",
            "phone": "رقم الجوال",
            "email": "البريد الإلكتروني",
            "message": "الرسالة",
        }

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone", "").strip()
        email = cleaned_data.get("email", "").strip()
        if not phone and not email:
            raise forms.ValidationError("يرجى إدخال رقم الجوال أو البريد الإلكتروني على الأقل.")
        return cleaned_data
