from django.views.generic import TemplateView


class PortfolioView(TemplateView):
    """Página con el portfolio, con la misma estética que el blog."""

    template_name = "pages/portfolio.html"
