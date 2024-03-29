from django.contrib import admin
from django.urls import path, include
from crm import views as crm_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # URL para login
    path('login/', crm_views.login_view, name='login'),
    # URL para logout
    path('logout/', crm_views.logout_view, name='logout'),
    # Incluindo as URLs do aplicativo 'crm'
    path('crm/', include('crm.urls')),
    # Redirecionamento para 'crm' se o usuário estiver logado
    path('', crm_views.home_view, name='home'),
]
