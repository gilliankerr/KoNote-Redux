"""Terminology middleware — makes term overrides available on request."""
from django.core.cache import cache


class TerminologyMiddleware:
    """
    Attach terminology lookup to request object so views can use
    request.term('target') to get the customised term.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Lazy-load terms (context processor handles template injection)
        request.get_term = self._get_term_func
        return self.get_response(request)

    @staticmethod
    def _get_term_func(key, default=None):
        """Look up a terminology override, falling back to default."""
        from apps.admin_settings.models import TerminologyOverride

        terms = cache.get("terminology_overrides")
        if terms is None:
            terms = TerminologyOverride.get_all_terms()
            cache.set("terminology_overrides", terms, 300)
        return terms.get(key, default or key)
