from appconf import AppConf
from django.conf import settings


class SkillsGuideAppConf(AppConf):
    COPYRIGHT = "Some Company"
    LZK_API_URL = "https://lernzielkatalog-medizin.at/api"
    LZK_API_CACHE_TIMEOUT = 3600

    class Meta:
        prefix = "SkillsGuide"
