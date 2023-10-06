from django.views.generic import TemplateView


class MenuTemplateView(TemplateView):
    """Представление для отображения меню."""
    template_name = 'main_menu.html'
