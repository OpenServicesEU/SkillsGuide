from appconf import AppConf
from django.conf import settings


class SkillsGuideAppConf(AppConf):
    COPYRIGHT = "Some Company"

    class Meta:
        prefix = "SkillsGuide"
