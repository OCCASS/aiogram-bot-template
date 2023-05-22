import re
from pathlib import Path

import jinja2

from src.data import settings


def render_template(template_name: str, *, context: dict | None = None, templates_path: Path | None = None) -> str:
    """
    Render jinja2 template
    :param template_name: name of jinja2 template
    :param context: context for template
    :param templates_path: path with templates
    """

    if context is None:
        context = {}
    template = _get_template_env(templates_path).get_template(template_name)
    rendered = template.render(**context).replace("\n", " ")
    rendered = rendered.replace("<br>", "\n")
    rendered = re.sub(" +", " ", rendered).replace(" .", ".").replace(" ,", ",")
    rendered = "\n".join(line.strip() for line in rendered.split("\n"))
    return rendered


def _get_template_env(templates_path: Path | None):
    if templates_path is None:
        templates_path = settings.TEMPLATES_DIR

    if not getattr(_get_template_env, "template_env", None):
        template_loader = jinja2.FileSystemLoader(searchpath=templates_path)
        env = jinja2.Environment(
            loader=template_loader,
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=True,
        )

        _get_template_env.template_env = env

    return _get_template_env.template_env
