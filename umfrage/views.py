from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.utils import simplejson
from fstools.extensions.templates import TemplateHelper
from jinja2 import Environment,  PackageLoader
from umfrage.models import Umfrage, Option, Vote
from django.contrib.auth.decorators import login_required

t = TemplateHelper('umfrage')

@login_required
def list(request):
    return t.render('list.djhtml', {'umfragen': Umfrage.objects.all(),}, req=request)

@login_required
def umfrage(request, umfrage_id):
    try:
        u = Umfrage.objects.get(pk=umfrage_id)
    except Umfrage.DoesNotExist:
        raise Http404

    if request.POST:
        response = {'success':True}
        messages.success(request, "Erfolgreich eingetragen")
        return HttpResponse(simplejson.dumps(response), mimetype='application/json')
    else:
        return t.render('umfrage.djhtml', {
                'umfrage': u,
                'optionen': u.optionen.all(),
                'votes': u.votes.all(),
                'currentuser': request.user
                }, req=request)
