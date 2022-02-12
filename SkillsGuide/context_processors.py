import requests
from django.core.cache import cache
from purl import URL

from .conf import settings as app_settings
from . import models


def settings(request):
    return {
        "login_url": app_settings.LOGIN_URL,
        "logout_url": app_settings.LOGOUT_URL,
        "copyright": app_settings.SKILLSGUIDE_COPYRIGHT,
    }


def navigation(request):
    clinical_traineeship_checklist_key = f"{__name__}/clinical_traineeship_checklist"
    clinical_traineeship_checklist = cache.get(clinical_traineeship_checklist_key)
    if clinical_traineeship_checklist is None:
        clinical_traineeship_checklist = dict()
        u = URL(
            app_settings.SKILLSGUIDE_LZK_API_URL
        ).add_path_segment(
            "skills"
        ).append_query_param(
            "clinical_traineeship_checklist",
            "True"
        ).as_string()
        s = requests.Session()
        s.headers.update({"Accept": "application/json"})
        while u:
            with requests.get(u, headers={"Accept": "application/json"}) as resp:
                data = resp.json()
                clinical_traineeship_checklist.update(
                    {obj.get("target"): obj.get("name") for obj in data.get("results")}
                )
                u = data.get("next")
        cache.set(
            clinical_traineeship_checklist_key,
            clinical_traineeship_checklist,
            app_settings.SKILLSGUIDE_LZK_API_CACHE_TIMEOUT
        )
    return {
        "top_downloads": models.Download.objects.filter(active=True, top=True),
        "chapters": models.Chapter.objects.all(),
        "clinical_traineeship_checklist": clinical_traineeship_checklist,
    }
