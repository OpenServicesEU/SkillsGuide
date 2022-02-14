import requests
from base64 import urlsafe_b64encode
from pathlib import PurePosixPath
from uuid import uuid4
from purl import URL
from memoize import memoize
from django.utils.text import slugify

from .conf import settings


class Uuid4Upload(str):
    def __new__(cls, instance, filename):
        f = PurePosixPath(filename)
        u = urlsafe_b64encode(uuid4().bytes).decode("ascii").rstrip("=")
        p = PurePosixPath(instance.__module__, instance._meta.object_name)
        return str.__new__(cls, p.joinpath(u).with_suffix(f.suffix))


@memoize(timeout=settings.SKILLSGUIDE_LZK_API_CACHE_TIMEOUT)
def load_clinical_traineeship_checklist():
    clinical_traineeship_checklist = dict()
    u = URL(
        settings.SKILLSGUIDE_LZK_API_URL
    ).add_path_segment(
        "activities"
    ).add_path_segment(
        ""
    ).as_string()
    s = requests.Session()
    s.headers.update({"Accept": "application/json"})
    while u:
        with s.get(u) as resp:
            data = resp.json()
        for activity in data.get("results"):
            pk = activity.get("url")
            clinical_traineeship_checklist[pk] = activity
            clinical_traineeship_checklist[pk]["skills"] = list()
        u = data.get("next")
    u = URL(
        settings.SKILLSGUIDE_LZK_API_URL
    ).add_path_segment(
        "skills"
    ).add_path_segment(
        ""
    ).append_query_param(
        "clinical_traineeship_checklist",
        "True"
    ).as_string()
    while u:
        with s.get(u) as resp:
            data = resp.json()
        for skill in data.get("results"):
            pk = skill.get("activity")
            clinical_traineeship_checklist[pk]["skills"].append(skill)
        u = data.get("next")
    return {slugify(a.get("name")): a for a in clinical_traineeship_checklist.values() if a.get("skills")}
