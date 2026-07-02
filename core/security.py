"""Security helpers shared by views, forms, and middleware."""

from functools import wraps

from PIL import Image, UnidentifiedImageError
from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import HttpResponseNotAllowed, JsonResponse
from django.utils.http import url_has_allowed_host_and_scheme


ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
ALLOWED_IMAGE_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
}


def safe_redirect_target(request, target, fallback="/"):
    """Return a same-site redirect target, falling back when input is unsafe."""
    target = (target or "").strip()
    if target and url_has_allowed_host_and_scheme(
        target,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return target
    return fallback


def json_get(view_func):
    """Require GET/HEAD and return JSON 405 for API clients."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.method not in {"GET", "HEAD"}:
            return JsonResponse({"detail": "Metodo nao permitido."}, status=405)
        return view_func(request, *args, **kwargs)

    return wrapper


def page_get(view_func):
    """Require GET/HEAD for read-only template pages."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.method not in {"GET", "HEAD"}:
            return HttpResponseNotAllowed(["GET", "HEAD"])
        return view_func(request, *args, **kwargs)

    return wrapper


def validate_image_upload(uploaded_file):
    """Validate admin image uploads by size, content type, extension, and bytes."""
    if not uploaded_file:
        return uploaded_file

    max_size = getattr(settings, "MAX_IMAGE_UPLOAD_SIZE", 5 * 1024 * 1024)
    if uploaded_file.size > max_size:
        raise ValidationError("Imagem muito grande. Envie um arquivo de ate 5 MB.")

    name = (uploaded_file.name or "").lower()
    if not any(name.endswith(ext) for ext in ALLOWED_IMAGE_EXTENSIONS):
        raise ValidationError("Formato de imagem nao permitido.")

    content_type = getattr(uploaded_file, "content_type", "")
    if content_type and content_type not in ALLOWED_IMAGE_CONTENT_TYPES:
        raise ValidationError("Tipo de arquivo de imagem invalido.")

    position = uploaded_file.tell() if hasattr(uploaded_file, "tell") else None
    try:
        image = Image.open(uploaded_file)
        image.verify()
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise ValidationError("Arquivo de imagem invalido ou corrompido.") from exc
    finally:
        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(position or 0)

    return uploaded_file
