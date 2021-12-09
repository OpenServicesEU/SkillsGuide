from pathlib import Path

from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django_libsass import OUTPUT_STYLE, SOURCE_COMMENTS, SassCompiler, compile, sass
from tinycss2.color3 import parse_color, RGBA

searched_locations = finders.searched_locations


class DjangoSassCompiler(SassCompiler):

    def __init__(self, content, attrs=None, filter_type=None, charset=None, filename=None):
        super().__init__(content=content, attrs=attrs, filter_type=filter_type, filename=filename)
        self.attrs = attrs

    def theme(self, key, fallback):
        #import pudb; pu.db
        color = self.attrs.get(f"theme-{key}")
        if not isinstance(color, str):
            return fallback
        parsed = parse_color(color)
        if not isinstance(parsed, RGBA):
            return fallback
        return sass.SassColor(
            parsed.red * 255,
            parsed.green * 255,
            parsed.blue * 255,
            parsed.alpha * 255
        )

    @staticmethod
    def importer(path, prev=None):
        # import pudb; pu.db

        # if not prev:
        #    result = finders.find(path)
        #    if result:
        #        return load(path, result)
        #    else:
        #        return None

        n = Path(path)
        p = Path(prev)
        for name in (
            n.with_suffix(".scss"),
            n.with_name(f"_{n.name}").with_suffix(".scss"),
        ):
            if p.is_absolute():
                search = str(name)
            else:
                search = str(p.parent / name)
            if not staticfiles_storage.exists(search):
                continue
            with staticfiles_storage.open(search) as content:
                return [(search, content.read())]

    def input(self, **kwargs):
        if self.filename:
            return compile(
                filename=self.filename,
                output_style=OUTPUT_STYLE,
                source_comments=SOURCE_COMMENTS,
                importers=[(0, DjangoSassCompiler.importer)],
                custom_functions={
                    "theme": lambda key, fallback: self.theme(key, fallback),
                },
            )
        else:
            return compile(
                string=self.content,
                output_style=OUTPUT_STYLE,
                source_comments=SOURCE_COMMENTS,
                importers=[(0, DjangoSassCompiler.importer)],
                custom_functions={
                    "theme": lambda key, fallback: self.theme(key, fallback),
                },
            )
