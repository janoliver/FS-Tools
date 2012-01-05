from rhp.models import *
from eval.models import Vlu
from django.contrib import admin

admin.site.register(Rhp, admin.ModelAdmin)
admin.site.register(Artikel, admin.ModelAdmin)
