#!/usr/bin/python2
# -*- coding: utf-8 -*-

from jingo import register

@register.filter
def none(value, replacement=''):
    if not value:
        return replacement
    return value

@register.filter
def date(value, format='%d.%m.%Y'):
    return value.strftime(format)
