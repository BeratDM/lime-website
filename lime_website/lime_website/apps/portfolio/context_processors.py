from .models import Portfolio


def portfolio_links(request):
    return {"portfolios": Portfolio.objects.all()}
