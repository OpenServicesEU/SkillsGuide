# Generated by Django 3.2.12 on 2022-02-14 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SkillsGuide', '0003_alter_chapter_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='text',
            name='placement',
            field=models.CharField(choices=[('homepage', 'Homepage'), ('about', 'About us'), ('clinical_traineeship_checklist', 'Clinical traineeship checklist')], default='homepage', max_length=32),
        ),
    ]
