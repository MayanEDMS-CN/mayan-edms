from __future__ import unicode_literals

from django.conf.urls import url
from .views import DocumentVersionRawView, DocumentVersionOnlineViewerRedirect, \
    DocumentOnlineViewerRedirect, DocumentEmbbedView

urlpatterns = [
    url(r'^version/(?P<pk>\d+)/raw/', DocumentVersionRawView.as_view(), name='document_version_raw'),
    url(r'^version/(?P<pk>\d+)/viewer/', DocumentVersionOnlineViewerRedirect.as_view(),
        name='document_version_online_viewer'),
    url(r'^document/(?P<pk>\d+)/viewer/', DocumentOnlineViewerRedirect.as_view(),
        name='document_online_viewer'),
    url(
        r'^document/(?P<pk>\d+)/embbed/$', DocumentEmbbedView.as_view(),
        name='document_embbed_viewer'
    ),
]
