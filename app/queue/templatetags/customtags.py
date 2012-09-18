# -*- coding: utf8 -*-
from django.template.defaultfilters import register

@register.filter(name='dictval')
def dictval(data, index):
    return data.get(index, u'')
