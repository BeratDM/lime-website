from django.urls import path

from . import views

app_name = "portfolio"
# urlpatterns = [
#     path("", views.gamedev, name="gamedev"),
# ]

urlpatterns = [
    path("<slug:portfolio_slug>/", views.portfolio_detail, name="portfolio_detail"),
]
