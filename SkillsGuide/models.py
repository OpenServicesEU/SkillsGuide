import logging
import magic
import mimeparse

from django.db import models
from django.dispatch import receiver
from django.urls import reverse_lazy as reverse
from django.utils.translation import gettext_lazy as _
from colorfield.fields import ColorField
from django_extensions.db.models import TimeStampedModel
from django_extensions.db.fields import AutoSlugField
from ordered_model.models import OrderedModel
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField

from .conf import settings
from .utils import Uuid4Upload

logger = logging.getLogger(__name__)


class CompetenceLevel(OrderedModel):
    title = models.CharField(_("Title"), max_length=256)
    acronym = models.CharField(_("Acronym"), max_length=6)
    slug = AutoSlugField(populate_from=["title"])

    class Meta(OrderedModel.Meta):
        pass

    def __str__(self):
        return self.title


class Chapter(OrderedModel):
    title = models.CharField(_("Title"), max_length=256)
    image = models.ImageField(upload_to=Uuid4Upload)
    dark = ColorField()
    light = ColorField()
    slug = AutoSlugField(populate_from=["title"])

    tags = TaggableManager(blank=True)

    class Meta(OrderedModel.Meta):
        pass

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('chapter-detail', kwargs={'slug': self.slug})


class Section(OrderedModel):
    chapter = models.ForeignKey("Chapter", on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=256)
    slug = AutoSlugField(populate_from=["title"])

    order_with_respect_to = "chapter"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        path = self.chapter.get_absolute_url()
        return f"{path}#{self.slug}"


class Article(OrderedModel):
    section = models.ForeignKey("Section", on_delete=models.CASCADE)
    competence_level = models.ForeignKey("CompetenceLevel", on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=256)
    description = RichTextField(_("Description"))
    revision = models.BooleanField(_("Revision"), default=False)
    slug = AutoSlugField(populate_from=["title"])

    order_with_respect_to = "section"

    class Meta(OrderedModel.Meta):
        pass

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'chapter': self.section.chapter.slug, "slug": self.slug})


class Source(models.Model):
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    authors = models.TextField()
    title = models.TextField()
    published = models.TextField()


class Image(models.Model):
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    description = models.TextField(_("Description"))
    file = models.ImageField(upload_to=Uuid4Upload)


class Video(models.Model):
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    description = models.TextField(_("Description"))
    file = models.FileField(upload_to=Uuid4Upload)


class Download(TimeStampedModel):
    title = models.CharField(max_length=128)
    description = RichTextField()
    active = models.BooleanField(default=True, verbose_name=_("Active"))
    top = models.BooleanField(default=False, verbose_name=_("Top-Download"))
    file = models.FileField(upload_to="uploads/")
    icon = models.TextField(default="file-o")

    class Meta:
        verbose_name = _("Download")
        verbose_name_plural = _("Downloads")

    def __str__(self):
        return self.title

    @staticmethod
    @receiver(models.signals.pre_save, sender="SkillsGuide.Download")
    def pre_save(sender, instance, raw, **kwargs):
        icons = {
            ("audio",): "file-audio-o",
            ("image",): "file-image-o",
            ("video",): "file-video-o",
            ("text",): "file-text-o",
            ("application", "pdf"): "file-pdf-o",
            ("application", "zip"): "file-archive-o",
        }
        instance.file.seek(0)
        mimetype = magic.from_buffer(instance.file.read(2048), mime=True)
        instance.file.seek(0)
        maintype, subtype, _ = mimeparse.parse_mime_type(mimetype)
        instance.icon = icons.get((maintype, subtype), icons.get((maintype,), "file-o"))


class Text(OrderedModel):

    HOMEPAGE = "homepage"
    ABOUT = "about"
    PLACEMENT_CHOICES = (
        (HOMEPAGE, _("Homepage")),
        (ABOUT, _("About us")),
    )

    title = models.CharField(max_length=128)
    body = RichTextField()
    placement = models.CharField(
        max_length=32,
        choices=PLACEMENT_CHOICES,
        default=HOMEPAGE,
    )
    order_with_respect_to = "placement"

    class Meta:
        verbose_name = _("Text")
        verbose_name_plural = _("Texts")

    def __str__(self):
        return f"{self.title} ({self.placement})"


class Slide(OrderedModel):
    title = models.CharField(max_length=128)
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to=Uuid4Upload)

    class Meta(OrderedModel.Meta):
        verbose_name = _("Slide")
        verbose_name_plural = _("Slides")

    def __str__(self):
        return self.title


class News(TimeStampedModel):
    title = models.CharField(max_length=128)
    body = RichTextField()
    datetime = models.DateTimeField(auto_now_add=True)
    active = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")
        ordering = ("-datetime",)

    def __str__(self):
        return self.title
