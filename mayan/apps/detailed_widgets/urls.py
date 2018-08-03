from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    RecentChangedDocumentListView, RecentAddedDocumentListView, \
    TaggedImportantDocumentRedirect, EmptyTaggedImportantDocumentListView
)

urlpatterns = [
    url(
        r'^recent/changed/document/list/$',
        RecentChangedDocumentListView.as_view(),
        name='recent_changed_list'
    ),
    url(
        r'^recent/added/document/list/$',
        RecentAddedDocumentListView.as_view(),
        name='recent_added_list'
    ),
    url(
        r'^important/empty/$',
        EmptyTaggedImportantDocumentListView.as_view(),
        name='empty_important_list'
    ),
    url(
        r'^important/rediect/$',
        TaggedImportantDocumentRedirect.as_view(),
        name='redirect_to_important_list'
    ),
]