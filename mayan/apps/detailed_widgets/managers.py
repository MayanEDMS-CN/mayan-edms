from __future__ import unicode_literals

from django.db import models


class DashboardDisplayedTagManager(models.Manager):

    def is_tag_displayed(self, tag):
        ins = self.model.objects.filter(tag=tag).last()
        return ins is not None

    def add_tag(self, tag):
        ins = self.model.objects.filter(tag=tag).last()
        if ins is None:
            self.model.objects.create(tag=tag)

    def remove_tag(self, tag):
        ins = self.model.objects.filter(tag=tag).last()
        if ins is not None:
            ins.delete()
