from django.urls import path
from . import views
from .view.orders import ServiceOrder_ListView, ServiceOrder_CreateView, ServiceOrder_DeleteView
from .view.orders import ServiceOrder_DetailView, ServiceOrder_UpdateView

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    # Página de gerenciamento dos clientes
    path('customers/', views.customers_view, name='customers'),
    path('customers/new/', views.customer_new_view, name='new_customer'),
    path('customers/details/<int:customer_id>/', views.customer_details_view, name='details_customer'),
    path('customers/edit/<int:customer_id>/', views.customer_edit_view, name='edit_customer'),
    path('customers/delete/<int:customer_id>/', views.customer_delete_view, name='delete_customer'),

    path('orders/', ServiceOrder_ListView.as_view(), name='orders'),
    path('orders/create/', ServiceOrder_CreateView.as_view(), name='create_order'),
    path('orders/detail/<int:pk>/', ServiceOrder_DetailView.as_view(), name='detail_order'),
    path('orders/update/<int:pk>/', ServiceOrder_UpdateView.as_view(), name='update_order'),
    path('orders/delete/<int:pk>/', ServiceOrder_DeleteView.as_view(), name='delete_order')
]