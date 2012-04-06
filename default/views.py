from django.http import Http404
from extensions.templates import TemplateHelper
from django.contrib.auth.decorators import login_required

t = TemplateHelper('default')

@login_required
def start(request):
    return t.render('start.djhtml')

@login_required
def wiki(request):
    return t.render('wiki.djhtml')

@login_required
def kalender(request):
    return t.render('kalender.djhtml')
