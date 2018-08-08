from __future__ import unicode_literals

from django.conf.urls import url
from .views import PagesPreviewJsonForDocumentListView

urlpatterns = [
    url(
        r'^document/(?P<pk>\d+)/pages/images.json',
        PagesPreviewJsonForDocumentListView.as_view(),
        name='page_images_json'
    ),
]