from django import forms
from django.utils.translation import gettext_lazy as _

from website.models import Message, NewsLetter, Application


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["name", "email", "message"]

    def save(self, *args, **kwargs):
        self.instance.create()
        return self.instance


class AddEmailForm(forms.Form):

    email = forms.EmailField(label=_("Email"))

    class Meta:
        fields = [
            "email"
        ]


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            "first_name",
            "last_name",
            "birthday",
            "email",
            "cv",
            "message",
        ]

    def save(self, *args, **kwargs):
        self.instance.create()
        return self.instance
