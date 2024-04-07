from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from .base import ContextMixin
from ..models import Customer, ServiceOrder

@method_decorator(login_required, name='dispatch')
class ViewBase(ContextMixin):
    """
    Classe base para visualizações de clientes.
    """
    model = Customer
    active_page = 'Customers'

class Customer_ListView(ViewBase, ListView):
    """
    Visualização para listar clientes.
    """
    template_name = "customers/list.html"
    context_object_name = 'customers'

    def get_queryset(self):
        """
        Obtém a queryset dos clientes, filtrando por consulta de pesquisa, se presente.
        """
        search_query = self.request.GET.get('search_query')

        if search_query:
            return Customer.objects.filter(Q(first_name__icontains=search_query) |
                                           Q(last_name__icontains=search_query) |
                                           Q(cpf__icontains=search_query))
        return super().get_queryset()

class Customer_CreateView(ViewBase, CreateView):
    """
    Visualização para criar um novo cliente.
    """
    template_name = "customers/create.html"
    fields = ["first_name", "last_name", "email", "phone", "address", "cpf"]
    success_url = reverse_lazy('customers')

    def form_valid(self, form):
        """
        Executa quando o formulário é válido. Exibe uma mensagem de sucesso.
        """
        cpf = form.cleaned_data['cpf']
        if not cpf.isdigit():
            form.add_error('cpf', 'CPF must contain only numbers.')
            return self.form_invalid(form)
        
        messages.success(self.request, 'Customer created successfully')
        return super().form_valid(form)

class Customer_DetailView(ViewBase, DetailView):
    """
    Visualização para exibir detalhes de um cliente.
    """
    template_name = "customers/details.html"
    context_object_name = 'customer'

    def get_context_data(self, **kwargs):
        """
        Adiciona dados de serviço ao contexto.
        """
        context = super().get_context_data(**kwargs)
        context['services'] = ServiceOrder.objects.filter(client=self.get_object())
        return context

class Customer_UpdateView(ViewBase, UpdateView):
    """
    Visualização para atualizar um cliente.
    """
    template_name = "customers/update.html"
    fields = ["first_name", "last_name", "email", "phone", "address", "cpf"]
    context_object_name = 'customer'

    def form_valid(self, form):
        """
        Executa quando o formulário é válido. Exibe uma mensagem de sucesso.
        """
        cpf = form.cleaned_data['cpf']
        if not cpf.isdigit():
            form.add_error('cpf', 'CPF must contain only numbers.')
            return self.form_invalid(form)
        
        messages.success(self.request, 'Customer updated successfully.')
        return super().form_valid(form)

class Customer_DeleteView(ViewBase, DeleteView):
    """
    Visualização para excluir um cliente.
    """
    template_name = "customers/delete.html"
    context_object_name = 'customer'
    success_url = reverse_lazy('customers')

    def post(self, request, *args, **kwargs):
        """
        Manipula a solicitação POST para excluir um cliente e exibe uma mensagem de sucesso.
        """
        messages.success(self.request, 'Customer deleted successfully')
        return super().post(request, *args, **kwargs)