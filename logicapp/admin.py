from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Ticket, EventTicket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "event",
        "price",
        "available_seats",
        "discount",
        "tax",
        "is_active",
        "created_by",
        "created_at",
    )

    list_filter = (
        "is_active",
        "event",
        "created_at",
    )

    search_fields = (
        "name",
        "event__title",
        "created_by__email",
        "created_by__first_name",
        "created_by__last_name",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
    )

    fieldsets = (
        ("Ticket Information", {
            "fields": (
                "name",
                "event",
                "price",
                "benefits",
                "available_seats",
                "discount",
                "tax",
                "is_active",
            )
        }),
        ("Audit Information", {
            "fields": (
                "created_by",
                "created_at",
                "updated_by",
                "updated_at",
            )
        }),
    )





from django.contrib import admin
from .models import Booking
# Register your models here.
@admin.register(Booking)
class BookingDetails(admin.ModelAdmin):
    list_display=[
        'id',
        'created_by',
        'event',
       
        'payment_status'
    ]


@admin.register(EventTicket)
class EventTicketAdmin(admin.ModelAdmin):
    list_display = (
        "ticket_number",
        "booking",
        "created_at",
        "pdf",
    )
    list_filter = (
        "created_at",
    )
    search_fields = (
        "ticket_number",
        "booking__id",
        "booking__user__username",  # Adjust based on your Booking model
    )
    readonly_fields = (
        "created_at",
    )
    ordering = (
        "-created_at",
    )

    fieldsets = (
        (
            "Ticket Information",
            {
                "fields": (
                    "booking",
                    "ticket_number",
                    "pdf",
                )
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "created_at",
                )
            },
        ),
    )