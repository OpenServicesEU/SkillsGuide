import logging

from crispy_forms.bootstrap import FormActions, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count, Q
from django.http import Http404
from django.urls import reverse_lazy as reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.generic import DetailView, ListView, TemplateView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django_filters.views import FilterMixin, FilterView
from django_tables2.views import SingleTableMixin
from haystack.generic_views import SearchView as BaseSearchView

from . import filters, models, tables
from .layout import IconButton

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = "SkillsGuide/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texts"] = models.Text.objects.filter(placement=models.Text.HOMEPAGE)
        return context


class AboutView(TemplateView):
    template_name = "SkillsGuide/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texts"] = models.Text.objects.filter(placement=models.Text.ABOUT)
        return context


class ChapterDetailView(DetailView):
    model = models.Chapter
    template_name = "SkillsGuide/chapter/detail.html"


class ArticleDetailView(DetailView):
    model = models.Article
    template_name = "SkillsGuide/article/detail.html"


class SearchView(BaseSearchView):
    template_name = "SkillsGuide/search.html"
    results_per_page = 10
