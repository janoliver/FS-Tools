#!/usr/bin/python2
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
import extensions.models as cmodels
from eval.models import Personal
from datetime import datetime


class PPPUmfrage(cmodels.Timestamped_Model):

    name = models.CharField(max_length=255)
    ppp_start = models.DateTimeField(default=datetime.now)
    ppp_end = models.DateTimeField(default=datetime.now)

    class Meta:

        verbose_name_plural = 'PPP Umfragen'


    def __unicode__(self):
        return self.name


class Student(cmodels.Timestamped_Model):
    
    umfrage = models.ForeignKey(PPPUmfrage, related_name='matrikelnummern',
                                null=True)
    matrikelnummer = models.CharField(max_length=255)
    geburtstag = models.DateTimeField()

    class Meta:

        verbose_name_plural = 'Matrikelnummern'


    def __unicode__(self):
        return self.titel


class Nominierung(cmodels.Timestamped_Model):

    umfrage = models.ForeignKey(PPPUmfrage, related_name='nominierungen',
                                null=True)
    typ = models.BooleanField()
    person = models.CharField(null=True, max_length=255)
    text = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return "Nominierung"


