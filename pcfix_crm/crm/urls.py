from django.urls import path
from . import views
from .view.orders import ServiceOrder_ListView, ServiceOrder_CreateView, ServiceOrder_DeleteView
from .view.orders import ServiceOrder_DetailView, ServiceOrder_UpdateView

from .view.customers import Customer_ListView, Customer_CreateView, Customer_DeleteView
from .view.customers import Customer_DetailView, Customer_UpdateView

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),

    # Páginas de gerenciamento dos clientes
    path('customers/', Customer_ListView.as_view(), name='customers'),
    path('customers/create/', Customer_CreateView.as_view(), name='create_customer'),
    path('customers/detail/<int:pk>/', Customer_DetailView.as_view(), name='detail_customer'),
    path('customers/update/<int:pk>/', Customer_UpdateView.as_view(), name='update_customer'),
    path('customers/delete/<int:pk>/', Customer_DeleteView.as_view(), name='delete_customer'),

    # Páginas de gerenciamento das ordens de serviço
    path('orders/', ServiceOrder_ListView.as_view(), name='orders'),
    path('orders/create/', ServiceOrder_CreateView.as_view(), name='create_order'),
    path('orders/detail/<int:pk>/', ServiceOrder_DetailView.as_view(), name='detail_order'),
    path('orders/update/<int:pk>/', ServiceOrder_UpdateView.as_view(), name='update_order'),
    path('orders/delete/<int:pk>/', ServiceOrder_DeleteView.as_view(), name='delete_order')
]