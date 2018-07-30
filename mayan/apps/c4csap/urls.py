from __future__ import unicode_literals

from django.conf.urls import url
from .views import RedirectToHomeView, TabMashupView, \
    RedirectToServiceItemsView, RedirectToServiceTabView, KBHomeView, \
    DocumentVersionRawView, DocumentVersionOnlineViewerRedirect, \
    DocumentOnlineViewerRedirect, \
    NoAccessView, DocumentEmbbedView

urlpatterns = [
    url(r'^service/ticket/tab/$', TabMashupView.as_view(), name='c4csap_ticket_tab'),
    url(r'^kbhome/$', KBHomeView.as_view(), name='c4csap_kb_home'),
    url(r'^no/access/$', NoAccessView.as_view(), name='c4csap_no_access'),
    url(r'^home/$', RedirectToHomeView.as_view(), name='c4csap_redirect_home'),
    url(r'^tab/$', RedirectToServiceTabView.as_view(), name='c4csap_redirect_service_tab'),
    url(r'^items/$', RedirectToServiceItemsView.as_view(), name='c4csap_redirect_service_items'),
    url(r'^document/version/(?P<pk>\d+)/raw/', DocumentVersionRawView.as_view(), name='document_version_raw'),
    url(r'^document/version/(?P<pk>\d+)/viewer/', DocumentVersionOnlineViewerRedirect.as_view(),
        name='document_version_online_viewer'),
    url(r'^document/(?P<pk>\d+)/viewer/', DocumentOnlineViewerRedirect.as_view(),
        name='document_online_viewer'),
    url(
        r'^document/(?P<pk>\d+)/embbed/$', DocumentEmbbedView.as_view(),
        name='document_embbed_viewer'
    ),
]
