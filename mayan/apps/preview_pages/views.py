from __future__ import absolute_import, unicode_literals

import logging
import json

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.urls import reverse
from django.views import View

from documents.models import Document
from documents.settings import setting_preview_size


class PagesPreviewJsonForDocumentListView(View):

    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]

        doc = Document.objects.filter(pk=pk).last()
        result  = []
        if doc is not None:
            ver = doc.latest_version
            for page in ver.pages.all().order_by("page_number"):

                url = "%s?size=%s" % (
                    reverse("rest_api:documentpage-image", kwargs={
                        'pk': doc.pk,
                        'version_pk': ver.pk,
                        'page_pk': page.pk
                    }),
                    setting_preview_size.value
                )

                result.append({
                    "href": url,
                    "title": _("%(document)s, Page %(page_number)d") % {
                        "document": doc,
                        "page_number": page.page_number
                    }
                })
        response = HttpResponse(json.dumps(result), content_type="application/json")
        return response