from django.contrib.sitemaps import Sitemap

from . import models

from django.urls import reverse


class StaticViewSitemap(Sitemap):
    protocol = "https"
    priority = 1.0
    changefreq = "monthly"

    def items(self):
        return [
            "index",
            "about",
        ]

    def location(self, item):
        return reverse(item)


class ChapterSitemap(Sitemap):
    protocol = "https"
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return models.Chapter.objects.all()


class ArticleSitemap(Sitemap):
    protocol = "https"
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return models.Article.objects.all()


# class SymptomSitemap(Sitemap):
#    protocol = "https"
#    changefreq = "monthly"
#    priority = 0.5
#
#    def items(self):
#        return models.Symptom.objects.filter(public=True)
#
#
# class SkillSitemap(Sitemap):
#    protocol = "https"
#    changefreq = "monthly"
#    priority = 0.5
#
#    def items(self):
#        return models.Skill.objects.all()
