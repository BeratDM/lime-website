from django.contrib import admin
from .models import Portfolio, Section, Content


class SectionInline(admin.TabularInline):
    model = Section
    extra = 1


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "order")
    ordering = ("order",)
    inlines = [SectionInline]


class ContentInline(admin.TabularInline):
    model = Content
    extra = 1


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "portfolio", "order")
    ordering = ("portfolio", "order")
    inlines = [ContentInline]


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "section", "order")
    ordering = ("section", "order")
