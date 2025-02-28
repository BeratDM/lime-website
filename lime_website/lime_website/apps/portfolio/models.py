from django.db import models
from django.utils.text import slugify
import bleach
from lxml import html as lxml_html
import html

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
    "video",
    "source",
]
ALLOWED_ATTRIBUTES = {
    "a": ["href", "target", "rel"],
    "img": ["src", "alt", "width", "height"],
    "code": ["class"],
    "span": ["class"],
    "div": ["class", "data-repo"],
    "iframe": [
        "src",
        "width",
        "height",
        "allowfullscreen",
        "frameborder",
        "allow",
        "referrerpolicy",
    ],
    "blockquote": ["class", "data-id", "lang", "data-context"],
    "video": ["preload", "loop", "playsinline ", "muted", "autoplay"],
    "source": ["src", "type"],
}
ALLOWED_PROTOCOLS = ["http", "https", "data"]

DEFAULT_IFRAME_SANDBOX = "allow-scripts allow-same-origin allow-popups"
DEFAULT_IMG_CLASS = "responsive-img cstm-border1"
DEFAULT_VIDEO_AUTOPLAY = "autoplay"


def clean_html(html_content):
    cleaned_html = bleach.clean(
        html_content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True
    )
    cleaned_html = html.unescape(cleaned_html)
    tree = lxml_html.fromstring(f"<div>{cleaned_html}</div>")

    for iframe in tree.findall(".//iframe"):
        if "sandbox" not in iframe.attrib:
            iframe.attrib["sandbox"] = DEFAULT_IFRAME_SANDBOX

    for img in tree.findall(".//img"):
        if "class" not in img.attrib:
            img.attrib["class"] = DEFAULT_IMG_CLASS

    cleaned_html = lxml_html.tostring(tree, encoding="unicode", method="html")
    fixed_html = cleaned_html.replace("<div><div>", "<div>").replace(
        "</div></div>", "</div>"
    )
    return fixed_html


class Portfolio(models.Model):
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


class Section(models.Model):
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="sections",
        null=True,
        blank=True,  # Allows the field to be optional in Django forms and the admin interface.
    )
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
