from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    EarnedHistory,
    ImageModel,
    NewUser,
    PackageModel,
    PackagePurchase,
    Quiz,
    ScratchCard,
    Spin,
    VisitWebsites,
)

# Register your models here.


@admin.register(ImageModel)
class ImageModelAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "uploaded_at",
        "image",
    )
    list_per_page = 10
    editable = ("image",)
    search_fields = ("user",)


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ("username", "email", "phone")
    list_filter = ("username", "email", "phone", "is_active", "is_staff")
    # ordering = ("-start_date",)
    # list_display = (
    #     "username",
    #     "email",
    #     "phone",
    # ) + UserAdmin.list_display

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "email",
                    "phone",
                    "password",
                    # "country",
                )
            },
        ),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        (
            "Personal",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "country",
                    "refferal",
                    "balance",
                    # "reffer_code",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "phone",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )


# Quiz admin
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = (
        "question",
        "answer",
        "point",
    )
    list_per_page = 10
    # exclude = ("question", "answer", "point")
    search_fields = ("question",)


# spin admin
@admin.register(Spin)
class SpinAdmin(admin.ModelAdmin):
    list_display = (
        "spin",
        "win_amount",
        "status",
    )
    list_per_page = 10
    search_fields = ("spin",)


# scratch card admin
@admin.register(ScratchCard)
class ScratchCardAdmin(admin.ModelAdmin):
    list_display = (
        "scratch",
        "win_amount",
        "status",
    )
    list_per_page = 10
    search_fields = ("scratch",)


# visit websites admin
@admin.register(VisitWebsites)
class VisitWebsitesAdmin(admin.ModelAdmin):
    list_display = (
        "url",
        "visit_ammount",
    )
    list_per_page = 10
    search_fields = ("url",)


# earned history admin
@admin.register(EarnedHistory)
class EarnedHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "title",
        "amount",
        "date",
    )
    list_per_page = 10
    search_fields = ("user", "title")


# package purchase admin
@admin.register(PackageModel)
class PackageModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "mining_speed",
        "validity",
    )
    list_per_page = 10
    search_fields = ("package_name", "price")
    editable = ("price", "name", "validity")


# package purchase admin
@admin.register(PackagePurchase)
class PackagePurchaseAdmin(admin.ModelAdmin):
    list_display = ("user", "package", "amount", "date", "status")
    list_per_page = 10
    search_fields = ("user", "package", "amount")
    # editable = ("user", "package", "date")


admin.site.register(NewUser, UserAdminConfig)
