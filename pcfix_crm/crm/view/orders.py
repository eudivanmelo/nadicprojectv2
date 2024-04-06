from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .base import ContextMixin
from ..models import ServiceOrder

class ViewBase(ContextMixin):
    """
    Classe base para visualizações de pedidos de serviço.
    """
    model = ServiceOrder
    active_page = 'Service Orders'


class ServiceOrder_ListView(ViewBase, ListView):
    """
    Visualização para listar pedidos de serviço.
    """
    template_name = "serviceorders/list.html"
    context_object_name = "serviceorders"

    def get_queryset(self):
        """
        Obtém a queryset dos pedidos de serviço, filtrando por consulta de pesquisa, se presente.
        """
        search_query = self.request.GET.get('search_query')

        if search_query:
            return ServiceOrder.objects.filter(client__first_name__icontains=search_query)
        return super().get_queryset()


class ServiceOrder_CreateView(ViewBase, CreateView):
    """
    Visualização para criar um novo pedido de serviço.
    """
    template_name = "serviceorders/create.html"
    fields = ['client', 'description']
    success_url = reverse_lazy('orders')

    def get_initial(self):
        """
        Define os valores iniciais do formulário, incluindo o cliente, se especificado na consulta GET.
        """
        initial = super().get_initial()
        for_client = self.request.GET.get('for_client')
        
        if for_client:
            initial['client'] = int(for_client)

        return initial

    def form_valid(self, form):
        """
        Executa quando o formulário é válido. Exibe uma mensagem de sucesso.
        """
        messages.success(self.request, 'Service order created successfully')
        return super().form_valid(form)
    

class ServiceOrder_DetailView(ViewBase, DetailView):
    """
    Visualização para exibir detalhes de um pedido de serviço.
    """
    template_name = "serviceorders/details.html"
    context_object_name = 'service'


class ServiceOrder_UpdateView(ViewBase, UpdateView):
    """
    Visualização para atualizar um pedido de serviço.
    """
    template_name = "serviceorders/update.html"
    context_object_name = 'service'
    fields = ['description', 'value', 'status']

    def form_valid(self, form):
        """
        Executa quando o formulário é válido. Exibe uma mensagem de sucesso.
        """
        messages.success(self.request, 'Service order updated successfully')
        return super().form_valid(form)
    

class ServiceOrder_DeleteView(ViewBase, DeleteView):
    """
    Visualização para excluir um pedido de serviço.
    """
    template_name = "serviceorders/delete.html"
    context_object_name = 'service'
    success_url = reverse_lazy('orders')

    def post(self, request, *args, **kwargs):
        """
        Manipula a solicitação POST para excluir um pedido de serviço e exibe uma mensagem de sucesso.
        """
        messages.success(self.request, 'Service order deleted successfully')
        return super().post(request, *args, **kwargs)