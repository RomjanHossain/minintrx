from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    EarnedHistory,
    ImageModel,
    NewUser,
    PackageModel,
    PackagePurchase,
    Quiz,
    RefferedModel,
    ScratchCard,
    Spin,
    VisitWebsites,
    WithdrowRequest,
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
        # ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
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
        # ("Referral", {"fields": ("reffer_code",)}),
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
    )
    list_per_page = 10
    search_fields = ("package_name", "price")
    editable = ("price", "name")


# package purchase admin
@admin.register(PackagePurchase)
class PackagePurchaseAdmin(admin.ModelAdmin):
    list_display = ("user", "package", "amount", "date", "status")
    list_per_page = 10
    search_fields = ("user", "package", "amount")
    # editable = ("user", "package", "date")


# withdrow request admin
@admin.register(WithdrowRequest)
class WithdrowRequestAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "amount",
        "date",
        "status",
    )
    list_per_page = 10
    search_fields = ("user", "amount", "status")
    # editable = ("user", "package", "date")


@admin.register(RefferedModel)
class RefferedModelAdmin(admin.ModelAdmin):
    list_display = (
        # "user",
        "reffered_by",
        "reffered_to",
        "amount",
        "date",
    )
    list_per_page = 10
    search_fields = (
        "reffered_by__username",
        "reffer_code",
        "reffered_to__username",
    )

    def display_reffered_users(self, obj):
        return ", ".join([user.username for user in obj.reffered_user.all()])

    display_reffered_users.short_description = "Referred Users"


admin.site.register(NewUser, UserAdminConfig)
