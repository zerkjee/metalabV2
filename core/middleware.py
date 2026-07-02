"""Small security middleware used by the project."""

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse


class LoginRateLimitMiddleware:
    """Throttle repeated login POSTs by IP, path, and submitted username."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        paths = getattr(settings, "RATE_LIMIT_LOGIN_PATHS", {"/login/", "/django-admin/login/"})
        if request.method == "POST" and request.path in paths:
            limit = getattr(settings, "RATE_LIMIT_LOGIN_ATTEMPTS", 8)
            window = getattr(settings, "RATE_LIMIT_LOGIN_WINDOW", 300)
            username = (request.POST.get("username") or "").strip().lower()
            remote_addr = request.META.get("REMOTE_ADDR", "unknown")
            key = f"login-rate:{remote_addr}:{request.path}:{username}"
            cache.add(key, 0, window)
            try:
                attempts = cache.incr(key)
            except ValueError:
                cache.set(key, 1, window)
                attempts = 1
            if attempts > limit:
                return HttpResponse(
                    "Muitas tentativas de login. Tente novamente em alguns minutos.",
                    status=429,
                    content_type="text/plain; charset=utf-8",
                )
        return self.get_response(request)


class SecurityHeadersMiddleware:
    """Add defense-in-depth headers that do not depend on edge configuration."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.setdefault("X-Content-Type-Options", "nosniff")
        response.setdefault("Referrer-Policy", "same-origin")
        response.setdefault("Permissions-Policy", "geolocation=(), microphone=(), camera=()")
        response.setdefault(
            "Content-Security-Policy",
            "object-src 'none'; base-uri 'self'; frame-ancestors 'self'; form-action 'self'",
        )
        return response
