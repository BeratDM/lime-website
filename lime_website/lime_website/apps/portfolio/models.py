from django.db import models
from django.utils.text import slugify
import bleach

ALLOWED_TAGS = [
    "p",
    "br",
    "ul",
    "ol",
    "li",
    "a",
    "img",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "strong",
    "em",
    "blockquote",
    "code",
    "pre",
    "span",
    "div",
]
ALLOWED_ATTRIBUTES = {
    "a": ["href", "target", "rel"],
    "img": ["src", "alt"],
    "code": ["class"],
    "span": ["class"],
    "div": ["class"],
}


def clean_html(html):
    return bleach.clean(
        html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True
    )


class Section(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.text:
            self.text = clean_html(self.text)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Content(models.Model):
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name="contents"
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.text:
            self.text = clean_html(self.text)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} (in {self.section.title})"
