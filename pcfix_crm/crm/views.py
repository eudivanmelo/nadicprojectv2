from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.http import HttpRequest
from django.shortcuts import render, redirect
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

def dashboard_view(request: HttpRequest):
    context = {'active_page': "Dashboard"}
    
    customers = Customer.objects.all()
    context.update({'customers': customers})
    
    serviceorders = ServiceOrder.objects.all()
    context.update({'serviceorders': serviceorders})
    
    context.update({'orderdelayed': count_ordersDelayed(ServiceOrder.objects.filter(status__in=['budgeting', 'approved_budget', 'under_maintenance']), 48)})
    context.update({'totalearnings': count_ordersEarning(ServiceOrder.objects.filter(status='delivered'))})
    context.update({'data_dashboard': generate_weekly_report()})
    
    return render(request, 'dashboard.html', context)
