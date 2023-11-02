from django.contrib import admin

from club.models import (
    Club, Plan, Subscription, Insurance,
    Member, Player, Guardian,
    Payment, Expense
)


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

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    pass

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass

@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
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
