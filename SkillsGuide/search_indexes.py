from haystack import indexes

from . import models


class ChapterIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    chapter = indexes.IntegerField(model_attr='pk')
    rendered = indexes.CharField(use_template=True, indexed=False)

    def get_model(self):
        return models.Chapter

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    chapter = indexes.IntegerField(model_attr='section__chapter__pk')
    rendered = indexes.CharField(use_template=True, indexed=False)

    def get_model(self):
        return models.Article

    def index_queryset(self, using=None):
        return self.get_model().objects.exclude(revision=True)
