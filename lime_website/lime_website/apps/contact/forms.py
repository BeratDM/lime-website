from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class ContactForm(forms.Form):
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Name"}),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Message", "rows": 5}
        ),
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={"data-theme": "dark"}))
