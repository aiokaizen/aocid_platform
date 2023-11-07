from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe

from easy_thumbnails.templatetags.thumbnail import thumbnail_url

from club.models import (
    Club, Plan, Subscription,
    Insurance, Committee,
    Member, CommitteeMember, Player, Guardian,
    Payment, Expense, Family,
    Book, Album, Media, Session
)


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
    readonly_fields = ( "photo_tag", )

    def photo_tag(self, obj):
        """ self.photo's HTML tag for use with Django Admin """
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
class ClubAdmin(admin.ModelAdmin):
    readonly_fields = ("sold", )
    list_display = (
        "__str__",
        "sold"
    )


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    pass


@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "amount"
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "date"
    )


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    pass


@admin.register(Member)
class MemberAdmin(PersonAdminMixin, admin.ModelAdmin):
    fields = [
        *PersonAdminMixin.fields,
        "user",
        "role",
    ]


@admin.register(CommitteeMember)
class CommitteeMemberAdmin(PersonAdminMixin, admin.ModelAdmin):
    fields = [
        *PersonAdminMixin.fields,
        "user",
        "player",
        "committee",
        "role",
    ]


@admin.register(Player)
class PlayerAdmin(PersonAdminMixin, admin.ModelAdmin):
    fields = [
        *PersonAdminMixin.fields,
        "guardian",
        "elo",
        "family",
    ]


@admin.register(Guardian)
class GuardianAdmin(PersonAdminMixin, admin.ModelAdmin):
    fields = [
        *PersonAdminMixin.fields,
        # "",
    ]


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    readonly_fields = [
        "payment_date"
    ]


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    readonly_fields = [
        "expense_date"
    ]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    pass


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    pass


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    filter_horizontal = ('absence_list',)
