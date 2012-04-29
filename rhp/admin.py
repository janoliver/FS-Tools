#!/usr/bin/python2
# -*- coding: utf-8 -*-
from rhp.models import *
from eval.models import Vlu
from django.contrib import admin

admin.site.register(Rhp, admin.ModelAdmin)
admin.site.register(Artikel, admin.ModelAdmin)
