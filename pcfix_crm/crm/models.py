from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

class Customer(models.Model):
    """
    Modelo para representar um cliente.

    Attributes:
        first_name (CharField): O primeiro nome do cliente.
        last_name (CharField): O sobrenome do cliente.
        email (EmailField): O endereço de e-mail do cliente.
        phone (CharField): O número de telefone do cliente.
        address (CharField): O endereço do cliente.
        cpf (CharField): O número do CPF do cliente.
        created_at (DateTimeField): A data e hora de criação do registro do cliente (auto_now_add=True).
    """

    first_name = models.CharField(max_length=50,
                                  help_text="First name of the customer.")
    last_name = models.CharField(max_length=50,
                                  help_text="Last name of the customer.")
    email = models.EmailField(help_text="Email address of the customer.")
    phone = models.CharField(max_length=20,
                              help_text="Phone number of the customer.")
    address = models.CharField(max_length=200,
                                help_text="Address of the customer.")
    cpf = models.CharField(max_length=11, unique=True,
                            help_text="CPF number of the customer.")
    created_at = models.DateTimeField(auto_now_add=True,
                                       help_text="Date and time when the customer record was created.")

    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
class ServiceOrder(models.Model):
    """
    Modelo para representar uma ordem de serviço.

    Attributes:
        client (ForeignKey): O cliente associado à ordem de serviço.
        description (TextField): A descrição da ordem de serviço.
        created_at (DateTimeField): A data e hora de criação da ordem de serviço (auto_now_add=True).
        concluded_at (DateTimeField): A data e hora de conclusão da ordem de serviço (pode ser nulo).
        value (DecimalField): O valor da ordem de serviço (pode ser nulo).
        status (CharField): O status atual da ordem de serviço.
    """

    client = models.ForeignKey(Customer, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    concluded_at = models.DateTimeField(null=True)
    value = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    status_choices = [('budgeting', 'Budgeting'),
                      ('approved_budget', 'Approved budget'),
                      ('under_maintenance', 'Under maintenance'),
                      ('concluded', 'Concluded'),
                      ('delivered', 'Delivered')]
    status = models.CharField(max_length=20, choices=status_choices, default='budgeting')
    
    def __str__(self):
        return f"Service Order for '{self.client}' - Status: {self.status}"
    
    def get_absolute_url(self):
        return reverse('detail_order', kwargs={'pk': self.pk})
    
@receiver(models.signals.pre_save, sender=ServiceOrder)
def update_concluded_at(sender, instance, **kwargs):
    """
    Atualiza o campo 'concluded_at' do objeto ServiceOrder quando o status é modificado antes de salvar.

    Args:
        sender (Model): O modelo que está emitindo o sinal.
        instance (ServiceOrder): A instância de ServiceOrder sendo salva.
        **kwargs: Argumentos adicionais.

    Returns:
        None
    """
    if instance.pk:  # Se o objeto já existe no banco de dados (não é uma criação)
        original_instance = sender.objects.get(pk=instance.pk)
        # Verifica se o status da instância original é diferente do status atual
        if original_instance.status != instance.status and instance.status == 'concluded':
            # Atualiza o campo 'updated_at' para o tempo atual
            instance.concluded_at = timezone.now()


