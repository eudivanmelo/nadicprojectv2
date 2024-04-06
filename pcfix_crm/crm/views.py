from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.db.models import Q

from .forms import CustomerSearchForm, CustomerForm
from .utils import log_message, count_ordersDelayed, count_ordersEarning, generate_weekly_report
from .models import Customer, ServiceOrder

def login_view(request: HttpRequest):
    """
    Exibe um formulário de login para os usuários e processa as tentativas de login.
    
    Args:
        request (HttpRequest): O objeto HttpRequest contendo os dados da solicitação HTTP.
        
    Returns:
        HttpResponse: Uma resposta HTTP renderizada com o formulário de login ou um redirecionamento bem-sucedido.
    """
    # Obtém o nome do campo de redirecionamento, se fornecido na solicitação GET.
    redirect_field_name = request.GET.get('next', None)

    if request.method == 'POST':
        # Se a solicitação é do tipo POST, tenta autenticar o usuário.
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # Se o formulário de autenticação é válido, realiza o login para o usuário.
            user = form.get_user()
            login(request, user)
            # Obtém o endereço IP do cliente, se disponível.
            ip_address = request.META.get('REMOTE_ADDR', None)
            # Registra uma mensagem de log sobre o login bem-sucedido.
            log_message(f"User '{user}' logged in. IP: {ip_address}")
            # Redireciona para a URL fornecida na solicitação GET ou para a página inicial do CRM.
            return redirect(redirect_field_name or 'dashboard')
    else:
        # Se a solicitação não é do tipo POST, exibe um formulário de autenticação vazio.
        form = AuthenticationForm()
    
    # Renderiza o template de login com o formulário (vazio ou com erros de validação).
    return render(request, 'login.html', {'form': form})

def logout_view(request: HttpRequest):
    """
    Realiza o logout do usuário e redireciona para a página de login.

    Args:
        request (HttpRequest): O objeto HttpRequest contendo os dados da solicitação HTTP.

    Returns:
        HttpResponseRedirect: Um redirecionamento HTTP para a página de login.
    """
    # Registra uma mensagem de log sobre o logout do usuário.
    log_message(f"User '{request.user}' logged out.")
    
    # Realiza o logout do usuário.
    logout(request)
    
    # Redireciona para a página de login.
    return redirect('login')

@login_required
def home_view(request: HttpRequest):
    """
    Exibe a página inicial do usuário.

    Requerimentos:
        O usuário deve estar autenticado.

    Args:
        request (HttpRequest): O objeto HttpRequest contendo os dados da solicitação HTTP.

    Returns:
        HttpResponseRedirect: Um redirecionamento HTTP para a página inicial do CRM.
    """
    # Redireciona para a página inicial do CRM.
    return redirect('dashboard')

@login_required
def dashboard_view(request: HttpRequest):
    """
    Exibe o painel de controle do usuário autenticado.

    Requerimentos:
        O usuário deve estar autenticado.

    Args:
        request (HttpRequest): O objeto HttpRequest contendo os dados da solicitação HTTP.

    Returns:
        HttpResponse: Uma resposta HTTP renderizada com o painel de controle.
    """
    # Inicializa o contexto com a página ativa como "Dashboard"
    context = {'active_page': "Dashboard"}
    
    # Recupera todos os clientes do banco de dados e os adiciona ao contexto
    customers = Customer.objects.all()
    context.update({'customers': customers})
    
    # Recupera todas as ordens de serviço do banco de dados e as adiciona ao contexto
    serviceorders = ServiceOrder.objects.all()
    context.update({'serviceorders': serviceorders})
    
    # Conta o número de ordens de serviço atrasadas e as adiciona ao contexto
    context.update({'orderdelayed': count_ordersDelayed(ServiceOrder.objects.filter(status__in=['budgeting', 'approved_budget', 'under_maintenance']), 48)})
    
    # Calcula o total de ganhos de todas as ordens de serviço entregues e as adiciona ao contexto
    context.update({'totalearnings': count_ordersEarning(ServiceOrder.objects.filter(status='delivered'))})
    
    # Gera e adiciona os dados do relatório semanal ao contexto
    context.update({'data_dashboard': generate_weekly_report()})
    
    # Renderiza o template 'dashboard.html' com o contexto e retorna a resposta HTTP
    return render(request, 'dashboard.html', context)

@login_required
def customers_view(request: HttpRequest):
    """
    Exibe uma lista de clientes e permite a pesquisa por clientes.

    Requerimentos:
        O usuário deve estar autenticado.

    Args:
        request (HttpRequest): O objeto HttpRequest contendo os dados da solicitação HTTP.

    Returns:
        HttpResponse: Uma resposta HTTP renderizada com a lista de clientes.
    """
    # Passa o contexto inicial da página
    context = {'active_page': "Customers"}
    
    # Inicializa um formulário de pesquisa de cliente com os dados da solicitação GET
    search_form = CustomerSearchForm(request.GET)
    context.update({'search_form': search_form})
    
    # Recupera todos os clientes do banco de dados
    customers = Customer.objects.all()

    # Se o formulário de pesquisa for válido e uma consulta de pesquisa for fornecida
    if search_form.is_valid() and search_form.cleaned_data['search_query']:
        search_query = search_form.cleaned_data['search_query']
        # Filtra os clientes com base na consulta de pesquisa
        customers = customers.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(cpf__icontains=search_query)
        )
    
    # Adiciona os clientes filtrados ou todos os clientes ao contexto
    context.update({'customers': customers})
    
    # Renderiza o template 'customers/customers_list.html' com o contexto e retorna a resposta HTTP
    return render(request, 'customers/customers_list.html', context)

@login_required
def customer_new_view(request: HttpRequest):
    """
    Exibe um formulário para adicionar um novo cliente e processa o envio do formulário.

    Requerimentos:
        O usuário deve estar autenticado.

    Args:
        request (HttpRequest): O objeto HttpRequest contendo os dados da solicitação HTTP.

    Returns:
        HttpResponse: Uma resposta HTTP renderizada com o formulário para adicionar um novo cliente ou redireciona para a página de clientes após a adição bem-sucedida de um novo cliente.
    """
    if request.method == 'POST':
        # Se o método da solicitação for POST, cria um formulário para adicionar um novo cliente com os dados fornecidos
        form = CustomerForm(request.POST)
        if form.is_valid():
            # Se o formulário for válido, salva os dados do novo cliente
            form.save()
            # Exibe uma mensagem de sucesso e redireciona para a página de clientes
            messages.success(request, "New client added successfully")
            return redirect('customers')
    else:
        # Se o método da solicitação não for POST, cria um formulário vazio para adicionar um novo cliente
        form = CustomerForm()
        
    # Define o contexto com a página ativa definida como "Customers" e o formulário para adicionar um novo cliente
    context = {'active_page': 'Customers', 
               'form': form}
    
    # Renderiza o template 'customers/new_customer.html' com o contexto e retorna a resposta HTTP
    return render(request, "customers/new_customer.html", context)

@login_required
def customer_details_view(request: HttpRequest, customer_id: int):
    """
    Exibe os detalhes de um cliente específico, incluindo todas as ordens de serviço associadas a esse cliente.

    Requerimentos:
        O usuário deve estar autenticado.

    Args:
        request (HttpRequest): O objeto HttpRequest contendo os dados da solicitação HTTP.
        customer_id (int): O ID do cliente cujos detalhes devem ser exibidos.

    Returns:
        HttpResponse: Uma resposta HTTP renderizada com os detalhes do cliente e todas as ordens de serviço associadas.
    """
    # Verifica se o cliente com o ID fornecido existe no banco de dados
    if Customer.objects.filter(id=customer_id).exists():
        # Se o cliente existe, recupera o objeto do cliente e todas as ordens de serviço associadas a ele
        customer = Customer.objects.get(id=customer_id)
        services = ServiceOrder.objects.filter(client=customer)
    else:
        # Se o cliente não existe, exibe uma mensagem de erro e redireciona de volta para a página de clientes
        messages.error(request, "Reported customer not found")
        return redirect('customers')
    
    # Define o contexto com a página ativa definida como "Customers", o objeto do cliente e todas as ordens de serviço associadas
    context = {'active_page': 'Customers',
               'customer': customer,
               'services': services}
    
    # Renderiza o template 'customers/customer_details.html' com o contexto e retorna a resposta HTTP
    return render(request, "customers/customer_details.html", context)

@login_required
def customer_edit_view(request: HttpRequest, customer_id: int):
    """
    Exibe um formulário para editar os detalhes de um cliente existente e processa a atualização dos detalhes do cliente.

    Requerimentos:
        O usuário deve estar autenticado.

    Args:
        request (HttpRequest): O objeto HttpRequest contendo os dados da solicitação HTTP.
        customer_id (int): O ID do cliente cujos detalhes devem ser editados.

    Returns:
        HttpResponse: Uma resposta HTTP renderizada com o formulário para editar os detalhes do cliente ou redireciona para a página de clientes após a atualização bem-sucedida dos detalhes do cliente.
    """
    # Verifica se o cliente com o ID fornecido existe no banco de dados
    if not Customer.objects.filter(id=customer_id).exists():
        # Se o cliente não existe, exibe uma mensagem de erro e redireciona de volta para a página de clientes
        messages.error(request, "Reported customer not found")
        return redirect('customers')
    
    # Recupera o objeto do cliente
    customer = Customer.objects.get(id=customer_id)
    
    if request.method == 'POST':
        # Se o método da solicitação for POST, isso significa que o formulário de edição foi enviado
        # Cria um formulário preenchido com os dados atuais do cliente
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            # Se o formulário for válido, salva os dados atualizados do cliente
            form.save()
            # Exibe uma mensagem de sucesso e redireciona para a página de clientes
            messages.success(request, 'Customer updated successfully.')
            return redirect('customers')
    else:
        # Se o método da solicitação não for POST, isso significa que o formulário de edição ainda não foi enviado
        # Cria um formulário preenchido com os dados atuais do cliente
        form = CustomerForm(instance=customer)

    # Define o contexto com a página ativa definida como "Customers", o objeto do cliente e o formulário de edição do cliente
    context = {'active_page': 'Customers', 
               'customer': customer,
               'form': form}

    # Renderiza o template 'customers/customer_edit.html' com o contexto e retorna a resposta HTTP
    return render(request, 'customers/customer_edit.html', context)

@login_required
def customer_delete_view(request: HttpRequest, customer_id: int):
    """
    Exibe um formulário para confirmar a exclusão de um cliente e processa a exclusão do cliente.

    Requerimentos:
        O usuário deve estar autenticado.

    Args:
        request (HttpRequest): O objeto HttpRequest contendo os dados da solicitação HTTP.
        customer_id (int): O ID do cliente que deve ser excluído.

    Returns:
        HttpResponse: Uma resposta HTTP renderizada com o formulário para confirmar a exclusão do cliente ou redireciona para a página de clientes após a exclusão bem-sucedida do cliente.
    """
    # Verifica se o cliente com o ID fornecido existe no banco de dados
    if not Customer.objects.filter(id=customer_id).exists():
        # Se o cliente não existe, exibe uma mensagem de erro e redireciona de volta para a página de clientes
        messages.error(request, "Reported customer not found")
        return redirect('customers')
    
    # Recupera o objeto do cliente
    customer = Customer.objects.get(id=customer_id)
    
    if request.method == 'POST':
        # Se o método da solicitação for POST, isso significa que o formulário de exclusão foi enviado
        # Exclui o cliente do banco de dados
        customer.delete()
        # Exibe uma mensagem de sucesso e redireciona para a página de clientes
        messages.success(request, 'Customer deleted successfully.')  
        return redirect('customers')
    else:
        # Se o método da solicitação não for POST, isso significa que o formulário de confirmação de exclusão ainda não foi enviado
        # Define o contexto com a página ativa definida como "Customers" e o objeto do cliente
        context = {'active_page': 'Customers', 
                   'customer': customer}
        # Renderiza o template 'customers/customer_delete.html' com o contexto e retorna a resposta HTTP
        return render(request, 'customers/customer_delete.html', context)
