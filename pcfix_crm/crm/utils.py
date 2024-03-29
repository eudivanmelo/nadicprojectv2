from django.utils import timezone
from django.db import models

def log_message(message):
    current_time = timezone.now().strftime('%d/%b/%Y %H:%M:%S')
    print(f"[{current_time}] \033[33m{message}\033[0m")
    
def count_ordersDelayed(orders, time):
    # Filtra as ordens de serviço que estão com mais de 48 horas
    orders_delayed = orders.filter(created_at__lte=timezone.now() - timezone.timedelta(hours=time))

    # Conta o número de ordens de serviço atrasadas
    return orders_delayed.count()

def count_ordersEarning(orders):
    # Calcula a soma dos valores dos serviços concluídos
    total_sum = orders.aggregate(total=models.Sum('value'))['total']

    # Se houver alguma ordem de serviço concluída
    if total_sum is None:
        total_sum = 0.00

    # Conta o número de ordens de serviço atrasadas
    return total_sum