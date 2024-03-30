from django.contrib import admin
from .models import Customer, ServiceOrder

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'address', 'cpf', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'address', 'created_at')

class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'description', 'status', 'created_at', 'value', 'concluded_at')
    list_filter = ('status',)
    search_fields = ('client__name', 'description')
    readonly_fields = ('created_at', 'concluded_at',)
    
admin.site.register(Customer, CustomerAdmin)
admin.site.register(ServiceOrder, ServiceOrderAdmin)
