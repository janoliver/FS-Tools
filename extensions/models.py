from django.contrib.contenttypes.models import ContentType
from django.db import models
from datetime import datetime


class Timestamped_Model(models.Model):
    date_created  = models.DateTimeField(editable=False, default=datetime.now)
    date_modified = models.DateTimeField(editable=False, default=datetime.now)

    class Meta:
        abstract = True

    def save(self):
        self.date_modified = datetime.now()
        super(Timestamped_Model, self).save()
