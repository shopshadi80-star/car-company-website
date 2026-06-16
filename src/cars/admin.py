from django.contrib import admin

from .models import Brand, Car, CarImage


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1
    fields = ("image", "is_main", "order")
    ordering = ("-is_main", "order")


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("__str__", "car_type", "status", "price", "city", "created_at")
    list_filter = ("car_type", "status", "brand", "fuel_type", "transmission", "origin")
    search_fields = ("brand__name", "model_name", "city")
    ordering = ("-created_at",)
    inlines = [CarImageInline]

    fieldsets = (
        ("معلومات أساسية", {
            "fields": ("car_type", "status", "brand", "model_name", "year"),
        }),
        ("التسعير", {
            "fields": ("price", "price_label"),
        }),
        ("السيارة الجديدة", {
            "classes": ("collapse",),
            "fields": ("trim", "features_summary"),
            "description": "حقول خاصة بالسيارات الجديدة فقط",
        }),
        ("السيارة المستعملة", {
            "classes": ("collapse",),
            "fields": (
                "mileage_km",
                "transmission",
                "fuel_type",
                "engine_size",
                "exterior_color",
                "origin",
                "city",
            ),
            "description": "حقول خاصة بالسيارات المستعملة فقط",
        }),
        ("الوصف", {
            "fields": ("description",),
        }),
    )


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ("car", "is_main", "order")
    list_filter = ("is_main",)
    search_fields = ("car__model_name", "car__brand__name")
    ordering = ("car", "-is_main", "order")
