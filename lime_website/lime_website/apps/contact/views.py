from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail

from lime_website.settings import DEFAULT_FROM_EMAIL
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
            send_mail(
                f"bu-contact-email",
                f"Contact Name:\n{name}\nContact Message:\n{message}",
                email,
                [DEFAULT_FROM_EMAIL],
            )
            return render(
                request, "contact.html", {"form": form, "contact_success": True}
            )

    else:
        raise NotImplementedError

    return render(request, "contact.html", {"form": form})
