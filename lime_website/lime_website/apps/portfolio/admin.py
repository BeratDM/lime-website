from django.contrib import admin
from .models import Section, Content


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    ordering = ("order",)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("title", "section", "order")
    ordering = ("section", "order")
