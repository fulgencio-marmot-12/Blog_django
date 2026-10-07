from django.views.generic import TemplateView


class PortfolioView(TemplateView):
    """Pagina con el portfolio, con la misma estatica que el blog."""

    template_name = "pages/portfolio.html"
