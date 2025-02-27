from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Portfolio


def portfolio_detail(request: HttpRequest, portfolio_slug: str) -> HttpResponse:
    portfolio = get_object_or_404(Portfolio, slug=portfolio_slug)
    sections = portfolio.sections.prefetch_related("contents").all()
    return render(
        request,
        "portfolio/portfolio_detail.html",
        {"portfolio": portfolio, "sections": sections},
    )
