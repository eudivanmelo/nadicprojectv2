from django import forms
from .models import Customer

class CustomerSearchForm(forms.Form):
    search_query = forms.CharField(label='Search', max_length=100)
    
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["first_name", "last_name", "email", "phone", "address", "cpf"]