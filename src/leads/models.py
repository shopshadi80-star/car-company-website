from django.db import models

from cars.models import Car


class LeadStatus(models.TextChoices):
    NEW = "new", "جديد"
    CONTACTED = "contacted", "تم التواصل"
    CLOSED = "closed", "مغلق"


class TestDriveRequest(models.Model):
    car = models.ForeignKey(
        Car,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"car_type": "new"},
        related_name="test_drive_requests",
        verbose_name="السيارة",
    )
    name = models.CharField(max_length=100, verbose_name="الاسم")
    phone = models.CharField(max_length=20, verbose_name="رقم الجوال")
    preferred_time = models.CharField(max_length=200, blank=True, verbose_name="الوقت المفضل")
    note = models.TextField(blank=True, verbose_name="ملاحظة")
    status = models.CharField(max_length=15, choices=LeadStatus.choices, default=LeadStatus.NEW, verbose_name="الحالة")
    internal_note = models.TextField(blank=True, verbose_name="ملاحظة داخلية")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "طلب تجربة قيادة"
        verbose_name_plural = "طلبات تجربة القيادة"
        ordering = ["-created_at"]

    def __str__(self):
        return f"تجربة قيادة — {self.name} ({self.phone})"


class InspectionRequest(models.Model):
    car = models.ForeignKey(
        Car,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"car_type": "used"},
        related_name="inspection_requests",
        verbose_name="السيارة",
    )
    name = models.CharField(max_length=100, verbose_name="الاسم")
    phone = models.CharField(max_length=20, verbose_name="رقم الجوال")
    preferred_time = models.CharField(max_length=200, blank=True, verbose_name="الوقت المفضل")
    note = models.TextField(blank=True, verbose_name="ملاحظة")
    status = models.CharField(max_length=15, choices=LeadStatus.choices, default=LeadStatus.NEW, verbose_name="الحالة")
    internal_note = models.TextField(blank=True, verbose_name="ملاحظة داخلية")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "طلب معاينة"
        verbose_name_plural = "طلبات المعاينة"
        ordering = ["-created_at"]

    def __str__(self):
        return f"معاينة — {self.name} ({self.phone})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="الاسم")
    phone = models.CharField(max_length=20, blank=True, verbose_name="رقم الجوال")
    email = models.EmailField(blank=True, verbose_name="البريد الإلكتروني")
    message = models.TextField(verbose_name="الرسالة")
    status = models.CharField(max_length=15, choices=LeadStatus.choices, default=LeadStatus.NEW, verbose_name="الحالة")
    internal_note = models.TextField(blank=True, verbose_name="ملاحظة داخلية")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "رسالة تواصل"
        verbose_name_plural = "رسائل التواصل"
        ordering = ["-created_at"]

    def __str__(self):
        return f"رسالة من {self.name}"
