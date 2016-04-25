from django import template
from django.utils.safestring import mark_safe
from django.template.base import resolve_variable, Node,TemplateSyntaxError

register = template.Library()


@register.simple_tag
def my_simple_time(v1,v2,v3):
    return v1 + v2 + v3


@register.simple_tag
def my_input(id_num, arg):
    result = "<input type='text' id='%s' class='%s' />".format(id_num, arg)
    return mark_safe(result)