from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    cpf = models.CharField(max_length=11)
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
class ServiceOrder(models.Model):
    client = models.ForeignKey(Customer, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    value = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('budgeting', 'Budgeting'), 
                                                      ('approved_budget', 'Approved budget'), 
                                                      ('under_maintenance', 'Under maintenance'), 
                                                      ('concluded', 'Concluded'),
                                                      ('delivered', 'Delivered')])
    
    def __str__(self):
        return f"Service Order for '{self.client}' - Status: {self.status}"


