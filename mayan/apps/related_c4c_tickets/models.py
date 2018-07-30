from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from documents.models import Document

@python_2_unicode_compatible
class C4CServiceTicket(models.Model):

    ticket_id = models.PositiveIntegerField(_("Ticket ID"), unique=True)
    title = models.CharField(_("Ticket Title"), blank=True, max_length=128)

    class Meta:
        verbose_name = _('C4C Ticket')
        verbose_name_plural = _('C4C Tickets')

    def __str__(self):
        return "%s" % self.ticket_id


@python_2_unicode_compatible
class DocumentServiceTicketRelatedSettings(models.Model):
    """
    Define the ticket relationship for a specific document should have
    """
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name='ticket_relationships',
        verbose_name=_('Document')
    )
    ticket = models.ForeignKey(
        C4CServiceTicket, on_delete=models.CASCADE, related_name="document_relationships",
        verbose_name=_("Ticket")
    )
    related = models.BooleanField(
        default=False,
        verbose_name=_('Does this article related to this ticket?')
    )

    class Meta:
        verbose_name = _('Document Ticket Relationship')
        verbose_name_plural = _('Document Ticket Relationships')

    def __str__(self):
        return "%s" % self.id
