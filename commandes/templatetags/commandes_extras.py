

#You can create a simple template tag to call any method with any arguments:

from django import template

register = template.Library()


@register.simple_tag
def get_total_for_user(commande, usser):
    return commande.total_for_user(usser)
