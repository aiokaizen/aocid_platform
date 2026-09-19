"""
Lightweight, dependency-free anti-spam helpers for public forms.

Two layers:

1. Honeypot -- a hidden field that real users never see but naive bots fill in.
   Add ``HoneypotMixin`` to a form and render a hidden ``website`` input in the
   template. When the field comes back non-empty the form stays *valid* but
   exposes ``is_bot = True`` so the view can silently drop the submission
   (pretending success so bots don't adapt).

2. Per-IP rate limiting -- ``is_rate_limited`` caps how often the same client
   can hit an endpoint. Uses Django's cache framework and django-ipware, both
   already available, so nothing new needs installing.
"""

import logging

from django import forms
from ipware import get_client_ip
from django.core.cache import cache

logger = logging.getLogger("errors")

# Name of the hidden honeypot input. Must match the template markup.
HONEYPOT_FIELD = "website"


class HoneypotMixin:
    """Adds a hidden honeypot field to a form.

    If the field is submitted with any value we assume a bot filled it and set
    ``self.is_bot`` -- without invalidating the form, so the view can decide to
    silently discard the submission.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_bot = False
        self.fields[HONEYPOT_FIELD] = forms.CharField(
            required=False, widget=forms.HiddenInput
        )

    def clean(self):
        cleaned = super().clean() or {}
        if cleaned.get(HONEYPOT_FIELD):
            self.is_bot = True
        return cleaned


def _client_ip(request):
    ip, _ = get_client_ip(request)
    return ip or "unknown"


def is_rate_limited(request, action, limit=5, period=3600):
    """Return True if this client has exceeded ``limit`` requests per ``period``.

    Fixed-window counter keyed by client IP and ``action``. Fails open: if the
    cache backend errors we let the request through rather than block a real
    user. ``period`` is in seconds (default 1 hour), ``limit`` submissions.
    """
    ip = _client_ip(request)
    key = f"antispam:{action}:{ip}"
    try:
        # First hit in the window: seed the counter with its TTL.
        if cache.add(key, 1, timeout=period):
            return False
        try:
            count = cache.incr(key)
        except ValueError:
            # Key expired between add() and incr(); start a fresh window.
            cache.add(key, 1, timeout=period)
            return False
        return count > limit
    except Exception as e:
        logger.error("antispam rate-limit error: %s", e)
        return False
