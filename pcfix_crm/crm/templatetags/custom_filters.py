from django import template

register = template.Library()

@register.filter(name='phone_format')
def phone_format(phone):
    if len(phone) == 11:
        return f'({phone[0:2]}) {phone[2:7]}-{phone[7:11]}'
    else:
        return phone  # Se o número de telefone não estiver no formato esperado, retorne como está

@register.filter(name='cpf_format')
def cpf_format(cpf):
    return f'{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}'
