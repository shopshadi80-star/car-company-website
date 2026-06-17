from django import forms

from .models import TestDriveRequest, InspectionRequest


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
