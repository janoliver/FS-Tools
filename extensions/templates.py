#!/usr/bin/python2
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from jinja2 import Environment, FileSystemLoader, PackageLoader, \
    ChoiceLoader
from django.template import RequestContext
from django.conf import settings
from django.utils import simplejson


class TemplateHelper:

    def __init__(self, app=None, folder='templates'):
        self.env = Environment(loader=ChoiceLoader([PackageLoader(app,
                               folder), PackageLoader('default')]),
                               extensions=list(settings.JINJA_EXTS))

        self.env.filters['date'] = self.datetimeformat
        self.env.filters['none'] = self.none

    def render(
        self,
        filename,
        context={},
        mimetype='text/html',
        req=None,
        ):
        args = context
        if req:
            for d in reversed(RequestContext(req, {}).dicts):
                args.update(d)
        template = self.env.get_template(filename)
        rendered = template.render(**args)
        return HttpResponse(rendered, mimetype=mimetype)

    def ajax(self, context={}, mimetype='application/json'):
        return HttpResponse(simplejson.dumps(context),
                            mimetype=mimetype)

    def datetimeformat(self, value, format='%d.%m.%Y'):
        return value.strftime(format)

    def none(self, value, replacement=''):
        if not value:
            return replacement
        return value


class LatexHelper:

    def __init__(self, loader):
        self.env = Environment(
            block_start_string='\BLOCK{',
            block_end_string='}',
            variable_start_string='\VAR{',
            variable_end_string='}',
            comment_start_string='\#{',
            comment_end_string='}',
            line_statement_prefix='%-',
            line_comment_prefix='%#',
            trim_blocks=True,
            autoescape=False,
            loader=loader,
            )

        self.env.filters['latexify'] = self.escapelatex
        self.env.filters['concat'] = self.concat
        self.env.filters['max'] = self.max_len
        self.env.filters['date'] = self.datetimeformat

    def escapelatex(self, string):
        replacements = {
            '<': '$<$',
            '>': '$>$',
            '%': '\%',
            '"': "''",
            }
        for (k, v) in replacements.iteritems():
            string = string.replace(k, v)
        string = '\\\\ \n'.join(string.splitlines())
        return string

    def concat(
        self,
        collection,
        divider=',',
        member='name',
        ):
        return divider.join([getattr(c, member) for c in collection])

    def max_len(self, list1, list2):
        if len(list1) > len(list2):
            return len(list1)
        return len(list2)

    def datetimeformat(self, value, format='%d.%m.%Y'):
        return value.strftime(format)


