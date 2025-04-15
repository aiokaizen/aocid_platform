from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe

from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from import_export.admin import ImportExportModelAdmin

from club.models import (
    Club,
    Plan,
    Subscription,
    Insurance,
    Committee,
    Member,
    CommitteeMember,
    Player,
    Guardian,
    Payment,
    Expense,
    Family,
    Book,
    Album,
    Media,
    Session,
)
from club.resources import PlayerResource


class PersonAdminMixin:
    fields = [
        ("photo_tag", "photo"),
        "first_name",
        "last_name",
        "birthday",
        "birth_place",
        "cnie",
        "chronic_disease",
        "disease_description",
        # Address
        # "country",
        "city",
        "postal_code",
        "street_address",
        # Contact informations
        "email",
        "phone_number",
        "fix_number",
        # Social Media
        "facebook_account",
        "instagram_account",
        "tiktok_account",
    ]
    readonly_fields = ("photo_tag",)

    def photo_tag(self, obj):
        """self.photo's HTML tag for use with Django Admin"""
        if obj.photo:
            return mark_safe(
                '<img src="%s" style="border-radius: 50%%;" />'
                % (thumbnail_url(obj.photo, "thumbnail"))
            )

        return mark_safe(
            """<div style="width: 30vw"><img
                src="/static/sandbox/assets/img/avatars/generic.jpeg"
                style="border-radius: 50%;" width="100"/></div>"""
        )

    photo_tag.short_description = _("Visualisation")


@admin.register(Club)
class ClubAdmin(ImportExportModelAdmin):
    readonly_fields = ("sold",)
    list_display = ("__str__", "sold")


@admin.register(Plan)
class PlanAdmin(ImportExportModelAdmin):
    pass


@admin.register(Insurance)
class InsuranceAdmin(ImportExportModelAdmin):
    list_display = ("__str__", "amount")


@admin.register(Subscription)
class SubscriptionAdmin(ImportExportModelAdmin):
    list_display = ("__str__", "date")


@admin.register(Committee)
class CommitteeAdmin(ImportExportModelAdmin):
    pass


@admin.register(Member)
class MemberAdmin(PersonAdminMixin, ImportExportModelAdmin):
    fields = [
        *PersonAdminMixin.fields,
        "user",
        "role",
    ]


@admin.register(CommitteeMember)
class CommitteeMemberAdmin(PersonAdminMixin, ImportExportModelAdmin):
    fields = [
        *PersonAdminMixin.fields,
        "user",
        "player",
        "committee",
        "role",
    ]


@admin.register(Player)
class PlayerAdmin(PersonAdminMixin, ImportExportModelAdmin):
    resource_classes = [PlayerResource]
    fields = [
        *PersonAdminMixin.fields,
        "guardian",
        "elo",
        "family",
    ]


@admin.register(Guardian)
class GuardianAdmin(PersonAdminMixin, ImportExportModelAdmin):
    fields = [
        *PersonAdminMixin.fields,
        # "",
    ]


@admin.register(Family)
class FamilyAdmin(ImportExportModelAdmin):
    pass


@admin.register(Payment)
class PaymentAdmin(ImportExportModelAdmin):
    readonly_fields = ["payment_date"]


@admin.register(Expense)
class ExpenseAdmin(ImportExportModelAdmin):
    readonly_fields = ["expense_date"]


@admin.register(Book)
class BookAdmin(ImportExportModelAdmin):
    pass


@admin.register(Album)
class AlbumAdmin(ImportExportModelAdmin):
    pass


@admin.register(Media)
class MediaAdmin(ImportExportModelAdmin):
    pass


@admin.register(Session)
class SessionAdmin(ImportExportModelAdmin):
    filter_horizontal = ("absence_list",)
