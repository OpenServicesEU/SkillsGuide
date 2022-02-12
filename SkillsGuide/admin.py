from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _
from ordered_model.admin import OrderedModelAdmin
from reversion.admin import VersionAdmin

from . import models

admin.sites.AdminSite.site_header = _("SkillsGuide")
admin.sites.AdminSite.site_title = _("Administration")
admin.sites.AdminSite.index_title = _("Administration")


@admin.register(models.Chapter)
class ChapterAdmin(VersionAdmin, OrderedModelAdmin):
    list_display = ("title", "move_up_down_links")


@admin.register(models.Section)
class SectionAdmin(VersionAdmin, OrderedModelAdmin):
    list_display = ("title", "move_up_down_links")
    list_filter = ("chapter",)
    search_fields = ("name",)


class ImageInline(admin.TabularInline):
    model = models.Image


class VideoInline(admin.TabularInline):
    model = models.Video


class SourceInline(admin.StackedInline):
    model = models.Source


@admin.register(models.Article)
class ArticleAdmin(VersionAdmin, OrderedModelAdmin):
    list_display = ("title", "section", "revision", "move_up_down_links")
    list_filter = ("section", "section__chapter", "revision")
    inlines = (ImageInline, VideoInline, SourceInline)


@admin.register(models.CompetenceLevel)
class CompetenceLevelAdmin(VersionAdmin, OrderedModelAdmin):
    list_display = ("title", "move_up_down_links")


@admin.register(models.Download)
class DownloadAdmin(admin.ModelAdmin):
    list_display = ("title", "active", "top")
    list_filter = ("active", "top")
    search_fields = ("title", "description")
    exclude = ("icon",)


@admin.register(models.Text)
class TextAdmin(OrderedModelAdmin):
    list_display = ("title", "placement")
    list_filter = ("placement",)
    search_fields = ("title", "body")


@admin.register(models.Slide)
class SlideAdmin(OrderedModelAdmin):
    list_display = ("title", "move_up_down_links")


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "active", "datetime")
    search_fields = ("title",)
