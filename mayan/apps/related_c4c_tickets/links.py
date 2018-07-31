from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link


link_document_edit_c4c_relationship = Link(
    text=_('Edit C4C Ticket Relationship'),
    view='related_c4c_tickets:document_create_relation', args='resolved_object.id'
)

link_document_create_c4c_relationship = Link(
    text=_('Create C4C Ticket Relationship'),
    view='related_c4c_tickets:relation_create', args='resolved_object.id'
)

link_document_list_c4c_relationship = Link(
    text=_('List C4C Ticket Relationship'),
    view='related_c4c_tickets:document_relation_list', args='resolved_object.id'
)

link_relation_delete = Link(
    args='resolved_object.id',
    text=_('Delete Relationship'), view='related_c4c_tickets:relation_delete'
)
