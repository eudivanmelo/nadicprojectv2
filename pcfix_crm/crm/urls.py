from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    # Página de gerenciamento dos clientes
    path('customers/', views.customers_view, name='customers'),
    path('customers/new/', views.customer_new_view, name='new_customer'),
    path('customers/details/<int:customer_id>/', views.customer_details_view, name='details_customer'),
    path('customers/edit/<int:customer_id>/', views.customer_edit_view, name='edit_customer'),
    path('customers/delete/<int:customer_id>/', views.customer_delete_view, name='delete_customer')


]