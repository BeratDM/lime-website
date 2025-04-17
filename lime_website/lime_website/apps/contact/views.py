from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail

from lime_website.settings import DEFAULT_EMAIL_TO, DEFAULT_EMAIL_FROM
import bleach
from . import forms


def contact(request: HttpRequest) -> HttpResponse:

    if request.method == "GET":
        form = forms.ContactForm()
    elif request.method == "POST":
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            name = bleach.clean(form.cleaned_data["name"])
            email = bleach.clean(form.cleaned_data["email"])
            message = bleach.clean(form.cleaned_data["message"])
            message_body = (
                f"Contact Name:\n{name}\n\n"
                f"Contact Mail Address:\n{email}\n\n"
                f"Contact Message:\n{message}\n"
            )
            send_mail(
                f"New Message Received From BU!",
                message_body,
                DEFAULT_EMAIL_FROM,
                [DEFAULT_EMAIL_TO],
            )
            return render(
                request, "contact.html", {"form": form, "contact_success": True}
            )

    else:
        raise NotImplementedError

    return render(request, "contact.html", {"form": form})
