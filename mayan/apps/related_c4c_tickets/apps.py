from __future__ import unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from acls import ModelPermission
from acls.permissions import permission_acl_edit, permission_acl_view
from common import (
    MayanAppConfig, menu_facet, menu_main, menu_multi_item, menu_object,
    menu_sidebar, menu_secondary
)
from navigation import SourceColumn

from .links import link_document_create_c4c_relationship, link_relation_delete, link_document_list_c4c_relationship

class RelatedC4CTickets(MayanAppConfig):
    has_tests = False
    name = "related_c4c_tickets"
    verbose_name = _('C4C Tickets')

    def ready(self):

        super(RelatedC4CTickets, self).ready()

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        DocumentVersion = apps.get_model(
            app_label='documents', model_name='DocumentVersion'
        )

        DocumentServiceTicketRelatedSettings = apps.get_model(
            app_label='related_c4c_tickets', model_name='DocumentServiceTicketRelatedSettings'
        )

        SourceColumn(
            source=DocumentServiceTicketRelatedSettings, label=_('Document'), attribute='document'
        )

        SourceColumn(
            source=DocumentServiceTicketRelatedSettings, label=_('C4C Ticket ID'), attribute='ticket'
        )

        SourceColumn(
            source=DocumentServiceTicketRelatedSettings, label=_('Related'), func=lambda context:_("True")
        )

        menu_object.bind_links(
            links=(link_document_create_c4c_relationship,), sources=(Document,)
        )

        menu_object.bind_links(
            links=(link_document_list_c4c_relationship,), sources=(Document,)
        )

        menu_object.bind_links(
            links=(link_relation_delete,), sources=(DocumentServiceTicketRelatedSettings,)
        )
