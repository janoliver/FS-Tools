#!/usr/bin/python2
# -*- coding: utf-8 -*-
from umfrage.models import Umfrage, Option
from eval.models import Vlu
from django.contrib import admin


class OptionInline(admin.TabularInline):

    model = Option
    extra = 3


class UmfrageAdmin(admin.ModelAdmin):

    inlines = [OptionInline]


admin.site.register(Umfrage, UmfrageAdmin)
