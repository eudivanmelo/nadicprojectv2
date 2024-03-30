from datetime import timedelta
from django.utils import timezone
from django.db import models
from .models import Customer, ServiceOrder

def log_message(message):
    """
    Registra uma mensagem de log formatada com o horário atual.

    Args:
        message (str): A mensagem a ser registrada no log.

    Returns:
        None
    """
    current_time = timezone.now().strftime('%d/%b/%Y %H:%M:%S')
    print(f"[{current_time}] \033[33m{message}\033[0m")
    
def count_ordersDelayed(orders, time):
    """
    Conta o número de ordens de serviço atrasadas com base em um determinado intervalo de tempo.

    Args:
        orders (QuerySet): Um QuerySet contendo as ordens de serviço.
        time (int): O número de horas após as quais uma ordem de serviço é considerada atrasada.

    Returns:
        int: O número de ordens de serviço consideradas atrasadas.
    """
    # Filtra as ordens de serviço que estão com mais de 48 horas
    orders_delayed = orders.filter(created_at__lte=timezone.now() - timezone.timedelta(hours=time))

    # Conta o número de ordens de serviço atrasadas
    return orders_delayed.count()

def count_ordersEarning(orders):
    """
    Calcula a soma dos valores dos serviços concluídos.

    Args:
        orders (QuerySet): Um QuerySet contendo as ordens de serviço concluídas.

    Returns:
        float: A soma dos valores dos serviços concluídos.
    """
    # Calcula a soma dos valores dos serviços concluídos
    total_sum = orders.aggregate(total=models.Sum('value'))['total']

    print(total_sum)
    # Se houver alguma ordem de serviço concluída
    if total_sum is None:
        total_sum = 0.00

    # Conta o número de ordens de serviço atrasadas
    return total_sum

def generate_weekly_report():
    """
    Gera um relatório semanal que contém estatísticas sobre clientes criados e ordens de serviço criadas e concluídas.

    Returns:
        dict: Um dicionário contendo os dados formatados para o relatório.
    """
    
    # Obtendo a data de início e fim da semana atual
    current_date = timezone.now()
    start_date = current_date - timedelta(days=current_date.weekday())
    end_date = start_date + timedelta(days=6)
    
    # Consulta ao banco de dados para recuperar os dados da semana atual
    customers = Customer.objects.filter(created_at__range=[start_date, end_date])
    customer_data = customers.annotate(created_count=models.Count('created_at', distinct=True))
    serviceorders = ServiceOrder.objects.filter(created_at__range=[start_date, end_date])
    service_order_data = serviceorders.annotate(
                            services_created=models.Count('created_at', distinct=True)
                        )
    serviceorders_concluded = ServiceOrder.objects.filter(concluded_at__range=[start_date, end_date])
    service_order_data_concluded = serviceorders_concluded.annotate(
                            services_completed=models.Count('concluded_at', distinct=True)
                        )
    
    # Inicializando listas para armazenar os dados do relatório
    labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    customers_created = [0] * 7
    services_created = [0] * 7
    services_completed = [0] * 7
    
    # Preenchendo os dados do relatório para clientes
    for datum in customer_data:
        day_of_week = datum.created_at.day - start_date.day
        customers_created[day_of_week] += datum.created_count
        
    # Preenchendo os dados do relatório para ordens de serviço
    for datum in service_order_data:
        day_of_week = datum.created_at.day - start_date.day
        services_created[day_of_week] += datum.services_created
    for datum in service_order_data_concluded:
        day_of_week = datum.concluded_at.day - start_date.day
        services_completed[day_of_week] += datum.services_completed
        

    # Dicionário contendo os dados formatados para o relatório
    chart_data = {
        'labels': labels,
        'datasets': [
            {
                'label': 'Customers Created',
                'data': customers_created,
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                'borderColor': 'rgba(255, 99, 132, 1)',
                'borderWidth': 1
            },
            {
                'label': 'Services Created',
                'data': services_created,
                'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                'borderColor': 'rgba(54, 162, 235, 1)',
                'borderWidth': 1
            },
            {
                'label': 'Services Completed',
                'data': services_completed,
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 1
            }
        ]
    }

    return chart_data




