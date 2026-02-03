"""Terminology middleware — makes term overrides available on request."""
from django.core.cache import cache
from django.utils.translation import get_language


class TerminologyMiddleware:
    """
    Attach terminology lookup to request object so views can use
    request.get_term('target') to get the customised term.

    The term is returned in the current language (from Django's i18n).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Lazy-load terms (context processor handles template injection)
        request.get_term = self._get_term_func
        return self.get_response(request)

    @staticmethod
    def _get_term_func(key, default=None, lang=None):
        """Look up a terminology override, falling back to default.

        Args:
            key: The terminology key (e.g., 'client', 'target').
            default: Fallback value if key not found.
            lang: Language code override. If None, uses current language.

        Returns:
            The customised term in the appropriate language.
        """
        from apps.admin_settings.models import TerminologyOverride

        # Determine language
        if lang is None:
            lang = get_language() or "en"
        lang_prefix = "fr" if lang.startswith("fr") else "en"
        cache_key = f"terminology_overrides_{lang_prefix}"

        terms = cache.get(cache_key)
        if terms is None:
            terms = TerminologyOverride.get_all_terms(lang=lang_prefix)
            cache.set(cache_key, terms, 300)
        return terms.get(key, default or key)
