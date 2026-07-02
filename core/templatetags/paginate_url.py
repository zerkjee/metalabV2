"""Filtro de template que preserva a querystring atual ao trocar de página.

Uso:
    {% load paginate_url %}
    <a href="?{% paginate_url request.GET page=2 %}">2</a>

Funciona com qualquer dicionário QueryDict (não só do request atual).
"""

from django import template
from django.http import QueryDict

register = template.Library()


@register.simple_tag
def paginate_url(querydict, **overrides):
    """Gera uma querystring preservando os parâmetros atuais.

    `overrides` sobrescreve valores (ex: page=2). Passar page=None
    remove o parâmetro `page` da URL.
    """
    if isinstance(querydict, QueryDict):
        params = {k: v for k, v in querydict.items() if v != ""}
    else:
        params = dict(querydict or {})
    for chave, valor in overrides.items():
        if valor is None:
            params.pop(chave, None)
        else:
            params[chave] = valor
    return "&".join(f"{k}={v}" for k, v in params.items()) if params else ""
