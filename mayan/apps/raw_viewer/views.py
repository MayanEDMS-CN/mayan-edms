from __future__ import absolute_import, unicode_literals

from django import VERSION as DJANGO_VERSION
from django.http import HttpResponse, Http404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View
import logging
from django.urls import reverse
from django.utils.decorators import method_decorator
from stronghold.decorators import public
from documents.models import DocumentVersion, Document
from documents.views import DocumentPreviewView
from c4csap.views import RedirectToPageView
from urllib import parse
from .forms import DocumentEmbbedViewForm



class DocumentVersionRawView(View):

    @method_decorator(public)
    def dispatch(self, request, *args, **kwargs):
        return super(DocumentVersionRawView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        vers = DocumentVersion.objects.get(pk=pk)
        data = vers.file.read()
        res = HttpResponse(data, content_type="%s; %s" % (vers.mimetype, "charset=UTF-8"))
        return res


class DocumentVersionOnlineViewerRedirect(RedirectToPageView):

    def get_redirect_url(self, *args, **kwargs):
        """
        Hide the static tag import to avoid errors with static file
        processors
        """
        pk = kwargs["pk"]
        host = self.request.META["HTTP_HOST"]
        embed_mode = int(self.request.GET.get("embed_mode", "0"))
        target_url = "http://%s%s" % (
            host, reverse("raw_viewer:document_version_raw", kwargs={"pk":pk})
        )
        vers = DocumentVersion.objects.get(pk=pk)
        if vers.mimetype in [
            'application/pdf',
            'application/xml',
            'text/x-c',
            'text/x-c++',
            'text/x-pascal',
            'text/x-msdos-batch',
            'text/x-python',
            'text/x-shellscript',
            'text/plain',
            'text/rtf',
        ]:
            redirect_url = target_url
        elif embed_mode == 1:
            redirect_url = "https://view.officeapps.live.com/op/embed.aspx?wdStartOn=1&wdZoomLevel=PageWidth&src=%s" % parse.quote(target_url)
        else:
            redirect_url = "https://view.officeapps.live.com/op/view.aspx?src=%s" % parse.quote(target_url)
        return redirect_url


class DocumentOnlineViewerRedirect(RedirectToPageView):

    def get_redirect_url(self, *args, **kwargs):
        """
        Hide the static tag import to avoid errors with static file
        processors
        """
        pk = kwargs["pk"]
        doc = Document.objects.get(pk=pk)
        if doc.latest_version is None:
            return Http404()
        redirect_url = reverse("raw_viewer:document_version_online_viewer", kwargs={"pk":doc.latest_version.id})
        return redirect_url


class DocumentEmbbedView(DocumentPreviewView):
    form_class = DocumentEmbbedViewForm
