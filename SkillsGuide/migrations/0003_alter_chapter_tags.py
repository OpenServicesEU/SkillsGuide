# Generated by Django 3.2.12 on 2022-02-12 20:17

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('SkillsGuide', '0002_news_slide'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]