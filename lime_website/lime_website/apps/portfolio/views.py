from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Section


def gamedev(request: HttpRequest) -> HttpResponse:
    sections = Section.objects.prefetch_related("contents").all()
    return render(request, "portfolio/gamedevportfolio.html", {"sections": sections})
