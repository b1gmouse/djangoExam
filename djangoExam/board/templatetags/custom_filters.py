from django import template


register = template.Library()

CURRENCIES_SYMBOLS = {
   'в': '*',
}


@register.filter()
def currency(value, code='в'):

   postfix = CURRENCIES_SYMBOLS[code]

   return f'{value} {postfix}'