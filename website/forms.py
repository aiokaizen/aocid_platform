from django import forms

from website.models import Message, NewsLetter, Application


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["name", "email", "message"]

    def save(self, *args, **kwargs):
        self.instance.create()
        return self.instance


class NewsLetterForm(forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = [
            "name",
            "emails"
        ]

    def save(self, *args, **kwargs):
        self.instance.create()
        return self.instance


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
