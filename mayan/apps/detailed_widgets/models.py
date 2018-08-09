from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model

from documents.models import Document
from tags.models import Tag
from .managers import DashboardDisplayedTagManager, FavouriteDocumentManager


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


@python_2_unicode_compatible
class FavouriteDocument(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favourites",
        verbose_name=_("User")
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="favouritees",
        verbose_name=_("Document")
    )
    added_datetime = models.DateTimeField(_("Added Datetime"), auto_now_add=True)

    objects = FavouriteDocumentManager()

    def __str__(self):
        return "%(user)s\'s favourite %(document)s" % {
            "user": self.user,
            "document": self.document
        }
