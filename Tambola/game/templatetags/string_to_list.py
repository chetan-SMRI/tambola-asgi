from django import template
import json, ast, re
register = template.Library()

@register.filter(name='to_list')
def to_list(arg):    
    list_of_no = ast.literal_eval(arg)    
    return list_of_no


@register.filter(name='replace_str')
def replace_str(arg):
    text = re.sub('[^a-zA-Z0-9 \n\.]', '', arg)
    return text