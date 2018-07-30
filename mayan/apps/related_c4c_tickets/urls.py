from __future__ import unicode_literals

from django.conf.urls import url
from .views import RelatedItemListView, C4CTicketRelationEditView, DocumentCreateRelationRedirectView, \
    C4CTicketRelationCreateView, C4CTicketDeleteConfirmView, C4CTicketRelationListView

urlpatterns = [
    url(
        r'^relation/(?P<pk>\d+)/delete/$',
        C4CTicketDeleteConfirmView.as_view(),
        name='relation_delete'
    ),
    url(
        r'^relation/(?P<pk>\d+)/edit/$',
        C4CTicketRelationEditView.as_view(),
        name='relation_edit'
    ),
    url(
        r'^relation/create/for/document/(?P<pk>\d+)/$',
        C4CTicketRelationCreateView.as_view(),
        name='relation_create'
    ),
    url(
        r'^document/(?P<pk>\d+)/redirect/to/relation/create/$',
        DocumentCreateRelationRedirectView.as_view(),
        name='document_create_relation'
    ),
    url(
        r'^document/(?P<pk>\d+)/relations/$',
        C4CTicketRelationListView.as_view(),
        name='document_relation_list'
    ),
    url(
        r'^service/ticket/kb_items/$',
        RelatedItemListView.as_view(),
        name='kb_items'),
]