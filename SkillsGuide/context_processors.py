from .conf import settings as app_settings
from . import models


def settings(request):
    return {
        "login_url": app_settings.LOGIN_URL,
        "logout_url": app_settings.LOGOUT_URL,
        "copyright": app_settings.SKILLSGUIDE_COPYRIGHT,
    }


def navigation(request):
    return {
        "top_downloads": models.Download.objects.filter(active=True, top=True),
        "chapters": models.Chapter.objects.all(),
    }
