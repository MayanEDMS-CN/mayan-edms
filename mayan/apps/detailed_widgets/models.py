from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from tags.models import Tag
from .managers import DashboardDisplayedTagManager


@python_2_unicode_compatible
class DashboardDisplayedTag(models.Model):

    tag = models.OneToOneField(Tag,
                               verbose_name=_("Document Tag"),
                               on_delete=models.CASCADE,
                               related_name="displayed_on_dashboard"
                               )
    added_datetime = models.DateTimeField(_("Added Datetime"), auto_now_add=True)

    objects = DashboardDisplayedTagManager()

    def __str__(self):
        return "%s" % self.tag
