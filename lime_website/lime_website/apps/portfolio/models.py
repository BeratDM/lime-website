from django.db import models
from django.utils.text import slugify
import bleach
from lxml import html

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
    "iframe",
]

ALLOWED_ATTRIBUTES = {
    "a": ["href", "target", "rel"],
    "img": ["src", "alt"],
    "code": ["class"],
    "span": ["class"],
    "div": ["class"],
    "iframe": [
        "src",
        "width",
        "height",
        "allowfullscreen",
        "frameborder",
        "allow",
        "referrerpolicy",
        "sandbox",
    ],
}

ALLOWED_PROTOCOLS = ["http", "https", "data"]


DEFAULT_SANDBOX = "allow-scripts allow-same-origin allow-popups"


def clean_html(html_content):
    cleaned_html = bleach.clean(
        html_content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True
    )

    # Parse the cleaned HTML with lxml to modify iframe attributes
    tree = html.fragment_fromstring(cleaned_html, create_parent="div")

    # Iterate over all <iframe> elements and enforce 'sandbox'
    for iframe in tree.findall(".//iframe"):
        if "sandbox" not in iframe.attrib:
            iframe.attrib["sandbox"] = DEFAULT_SANDBOX  # Apply default sandbox policy

    # Convert the modified tree back to a string
    return html.tostring(tree, encoding="unicode", method="html")


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
        if self.description:
            self.description = clean_html(self.description)
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
