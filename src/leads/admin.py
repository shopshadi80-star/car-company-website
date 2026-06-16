from django.contrib import admin

from .models import ContactMessage, InspectionRequest, LeadStatus, TestDriveRequest


class LeadMixin:
    """حقول وفلاتر مشتركة لجميع نماذج الطلبات."""
    list_display = ("name", "phone", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name", "phone")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)


@admin.register(TestDriveRequest)
class TestDriveRequestAdmin(LeadMixin, admin.ModelAdmin):
    list_display = ("name", "phone", "car", "status", "created_at")
    list_filter = ("status",)
    fieldsets = (
        ("بيانات العميل", {
            "fields": ("name", "phone", "preferred_time", "note"),
        }),
        ("السيارة", {
            "fields": ("car",),
        }),
        ("إدارة الطلب", {
            "fields": ("status", "internal_note", "created_at"),
        }),
    )


@admin.register(InspectionRequest)
class InspectionRequestAdmin(LeadMixin, admin.ModelAdmin):
    list_display = ("name", "phone", "car", "status", "created_at")
    list_filter = ("status",)
    fieldsets = (
        ("بيانات العميل", {
            "fields": ("name", "phone", "preferred_time", "note"),
        }),
        ("السيارة", {
            "fields": ("car",),
        }),
        ("إدارة الطلب", {
            "fields": ("status", "internal_note", "created_at"),
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name", "phone", "email")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
    fieldsets = (
        ("بيانات العميل", {
            "fields": ("name", "phone", "email", "message"),
        }),
        ("إدارة الطلب", {
            "fields": ("status", "internal_note", "created_at"),
        }),
    )
