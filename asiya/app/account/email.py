from djoser import email

from config import settings


def _build_site_url():
    domain = str(settings.DOMAIN).strip().rstrip("/")
    if domain.startswith("http://") or domain.startswith("https://"):
        return domain
    return f"https://{domain}"


class ActivationEmail(email.ActivationEmail):
    template_name = 'account/activation.html'

    def get_context_data(self):
        context = super().get_context_data()
        context["site_url"] = _build_site_url()
        return context
