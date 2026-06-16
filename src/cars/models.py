from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="الماركة")

    class Meta:
        verbose_name = "ماركة"
        verbose_name_plural = "الماركات"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم الفرع")
    city = models.CharField(max_length=100, verbose_name="المدينة")
    address = models.TextField(blank=True, verbose_name="العنوان")
    phone = models.CharField(max_length=20, blank=True, verbose_name="الهاتف")
    whatsapp = models.CharField(max_length=20, blank=True, verbose_name="واتساب")

    class Meta:
        verbose_name = "فرع"
        verbose_name_plural = "الفروع"
        ordering = ["city", "name"]

    def __str__(self):
        return f"{self.name} — {self.city}"


class Car(models.Model):
    class CarType(models.TextChoices):
        NEW = "new", "جديدة"
        USED = "used", "مستعملة"

    class Status(models.TextChoices):
        AVAILABLE = "available", "متاحة"
        HIDDEN = "hidden", "مخفية"
        SOLD = "sold", "مباعة"

    class Transmission(models.TextChoices):
        AUTOMATIC = "automatic", "أوتوماتيك"
        MANUAL = "manual", "يدوي"

    class FuelType(models.TextChoices):
        PETROL = "petrol", "بنزين"
        DIESEL = "diesel", "ديزل"
        HYBRID = "hybrid", "هجين"
        ELECTRIC = "electric", "كهربائي"

    class Origin(models.TextChoices):
        SAUDI = "saudi", "سعودي"
        GULF = "gulf", "خليجي"
        IMPORTED = "imported", "مستورد"

    # Core
    car_type = models.CharField(max_length=10, choices=CarType.choices, verbose_name="نوع السيارة")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.AVAILABLE, verbose_name="الحالة")
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name="الماركة")
    model_name = models.CharField(max_length=100, verbose_name="الموديل")
    year = models.PositiveSmallIntegerField(verbose_name="السنة")

    # Pricing
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="السعر")
    price_label = models.CharField(max_length=50, blank=True, verbose_name="تسمية السعر", help_text='مثال: ابتداءً من')

    # New-car extras
    trim = models.CharField(max_length=100, blank=True, verbose_name="الفئة (Trim)")
    features_summary = models.TextField(blank=True, verbose_name="مواصفات مختصرة")

    # Used-car fields
    mileage_km = models.PositiveIntegerField(null=True, blank=True, verbose_name="الممشى (كم)")
    transmission = models.CharField(max_length=15, choices=Transmission.choices, blank=True, verbose_name="ناقل الحركة")
    fuel_type = models.CharField(max_length=15, choices=FuelType.choices, blank=True, verbose_name="نوع الوقود")
    engine_size = models.CharField(max_length=20, blank=True, verbose_name="حجم المحرك")
    exterior_color = models.CharField(max_length=50, blank=True, verbose_name="اللون الخارجي")
    origin = models.CharField(max_length=15, choices=Origin.choices, blank=True, verbose_name="الوارد / المواصفات")
    branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="الفرع / المدينة")

    # Shared
    description = models.TextField(blank=True, verbose_name="وصف مختصر")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "سيارة"
        verbose_name_plural = "السيارات"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.brand} {self.model_name} {self.year} ({self.get_car_type_display()})"

    @property
    def is_visible(self):
        return self.status == self.Status.AVAILABLE


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="images", verbose_name="السيارة")
    image = models.ImageField(upload_to="cars/", verbose_name="الصورة")
    is_main = models.BooleanField(default=False, verbose_name="صورة رئيسية")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="الترتيب")

    class Meta:
        verbose_name = "صورة سيارة"
        verbose_name_plural = "صور السيارات"
        ordering = ["-is_main", "order"]

    def __str__(self):
        return f"صورة {self.car} {'(رئيسية)' if self.is_main else ''}"
