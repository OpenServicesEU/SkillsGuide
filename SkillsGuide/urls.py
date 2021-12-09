"""
SkillsGuide URL Configuration
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from . import sitemaps, views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("saml2/", include(("djangosaml2.urls", "saml2"), namespace="saml2")),
    path(
        "sitemap.xml",
        sitemap,
        {
            "sitemaps": {
                "static": sitemaps.StaticViewSitemap,
                "chapters": sitemaps.ChapterSitemap,
                "articles": sitemaps.ArticleSitemap,
            }
        },
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("", views.IndexView.as_view(), name="index"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("<str:slug>/", views.ChapterDetailView.as_view(), name="chapter-detail"),
    path("<str:chapter>/<str:slug>", views.ArticleDetailView.as_view(), name="article-detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
