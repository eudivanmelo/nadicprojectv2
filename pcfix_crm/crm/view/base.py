from django.views.generic import View

class ContextMixin(View):
    """
    Mixin para adicionar dados de contexto comuns a todas as views.

    Attributes:
        active_page (str): O nome da página ativa que será adicionada ao contexto.
    """
    # Atributos

    active_page = None

    # Metodos

    def get_context_data(self, **kwargs):
        """
        Retorna um dicionário com os dados de contexto para a view.

        Returns:
            dict: Um dicionário contendo os dados de contexto para a view.
        """
        context = super().get_context_data(**kwargs)
        context["active_page"] = self.active_page
        return context
    