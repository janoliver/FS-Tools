from eval.models import *
from django.contrib import admin

class OptionInline(admin.TabularInline):
    model = Option
    extra = 3

class VorlesungInline(admin.TabularInline):
    model = Vorlesung
    extra = 3

class FragenInline(admin.TabularInline):
    model = FrageFragenset
    extra = 3

class FragensetInline(admin.TabularInline):
    model = FragensetFragebogen
    extra = 3
    
        
class FragentypAdmin(admin.ModelAdmin):
    inlines = [OptionInline]


class VluAdmin(admin.ModelAdmin):
    inlines = [VorlesungInline]

class FragensetAdmin(admin.ModelAdmin):
    inlines = [FragenInline]

class FragebogenAdmin(admin.ModelAdmin):
    inlines = [FragensetInline]

    
admin.site.register(Studiengang, admin.ModelAdmin)
admin.site.register(Personal, admin.ModelAdmin)
admin.site.register(Personaltyp, admin.ModelAdmin)
admin.site.register(Fragentyp, FragentypAdmin)
admin.site.register(Vlu, VluAdmin)
admin.site.register(Fragenset, FragensetAdmin)
admin.site.register(Frage, admin.ModelAdmin)
admin.site.register(Vorlesung, admin.ModelAdmin)
admin.site.register(Fragebogen, FragebogenAdmin)
