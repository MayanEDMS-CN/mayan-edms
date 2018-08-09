from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    RecentChangedDocumentListView, RecentAddedDocumentListView,
    TaggedDocumentDashboardRedirect, EmptyTaggedDocumentListDashboardView,
    MessageDisplayDetail, MessageDisplayList, DashboardDisplayedTagAddConfirmView,
    DashboardDisplayedTagRemoveConfirmView, FavouriteDocumentAddConfirmView,
    FavouriteDocumentRemoveConfirmView, FavouriteDocumentListView
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
        r'^tagged/(?P<pk>\d+)/empty/$',
        EmptyTaggedDocumentListDashboardView.as_view(),
        name='empty_tagged_list'
    ),
    url(
        r'^tagged/(?P<pk>\d+)/rediect/$',
        TaggedDocumentDashboardRedirect.as_view(),
        name='redirect_to_tagged_list'
    ),
    url(
        r'^motd/list/$',
        MessageDisplayList.as_view(),
        name='motd_list'
    ),
    url(
        r'^motd/(?P<pk>\d+)/detail/$',
        MessageDisplayDetail.as_view(),
        name='motd_detail'
    ),
    url(
        r'^dashboard/add/tag/(?P<pk>\d+)/$',
        DashboardDisplayedTagAddConfirmView.as_view(),
        name='dashboard_add_tag'
    ),
    url(
        r'^dashboard/remove/tag/(?P<pk>\d+)/$',
        DashboardDisplayedTagRemoveConfirmView.as_view(),
        name='dashboard_remove_tag'
    ),
    url(
        r'^document/(?P<pk>\d+)/add/favourite/$',
        FavouriteDocumentAddConfirmView.as_view(),
        name='document_add_favourite'
    ),
    url(
        r'^document/(?P<pk>\d+)/remove/favourite/$',
        FavouriteDocumentRemoveConfirmView.as_view(),
        name='document_remove_favourite'
    ),
    url(
        r'^favourite/documents/$',
        FavouriteDocumentListView.as_view(),
        name='favourite_document_list'
    ),
]