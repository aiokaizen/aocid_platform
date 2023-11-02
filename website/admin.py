from django.contrib import admin

from website.models import Message, Slide, Button, Counter, NewsLetter, Application


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "message", "sent_date", "sent_by_mail"]
    fields = ["name", "email", "message", "sent_date", "sent_by_mail"]
    readonly_fields = ["sent_date", "sent_by_mail"]


@admin.register(Button)
class ButtonAdmin(admin.ModelAdmin):
    list_display = ["title", "action", "type", "slide"]
    fields = ["title", "action", "type", "slide"]


class ButtonInline(admin.StackedInline):
    model = Button
    max_num = 2


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ["title", "image", "description", "alignment"]
    fields = ["title", "image", "description", "alignment"]
    inlines = [ButtonInline]


@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    list_display = ["title", "icon", "count_to"]
    fields = ["title", "icon", "count_to"]


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ["name"]
    fields = ["name", "emails"]


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "birthday", "email", "cv"]
    fields = [
        "first_name",
        "last_name",
        "birthday",
        "email",
        "cv",
        "message",
    ]
