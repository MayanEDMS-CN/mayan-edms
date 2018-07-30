from __future__ import absolute_import, unicode_literals

from django import VERSION as DJANGO_VERSION
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView, TemplateView, View
import logging
from django.template import RequestContext
from django.urls import reverse
from django.utils.decorators import method_decorator
from stronghold.decorators import public
from braces.views._access import AccessMixin
from django.contrib.auth import authenticate, login, logout

from common.generics import SingleObjectEditView
from documents.models import DocumentVersion, Document
from documents.views import DocumentPreviewView
from urllib import parse
from .forms import DocumentEmbbedViewForm

if DJANGO_VERSION >= (1, 10, 0):
    _is_authenticated = lambda user: user.is_authenticated  # noqa
else:
    # Django<1.10 compatibility
    _is_authenticated = lambda user: user.is_authenticated()  # noqa


class NoAccessView(TemplateView):
    template_name = 'c4csap/no_access.html'

    @method_decorator(public)
    def dispatch(self, request, *args, **kwargs):
        return super(NoAccessView, self).dispatch(request, *args, **kwargs)


class C4CSAPTokenLoginMixin(AccessMixin):

    @method_decorator(public)
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        if "ticketid" in request.GET and len(request.GET["ticketid"])>0:
            request.session["ticketid"] = request.GET["ticketid"]
        c4c_username = request.GET.get("username", "")
        c4c_token = request.GET.get("token", "")
        if len(c4c_username)>0 and len(c4c_token)>0:
            user = authenticate(username=c4c_username, password=c4c_token)
            # user = authenticate(username="testkb", password="Welcome1")
            if user is not None:
                if _is_authenticated(request.user) and request.user != user:
                    logout(request)
                login(request, user)
                return super(C4CSAPTokenLoginMixin, self).dispatch(request, *args, **kwargs)

        return redirect("c4csap:c4csap_no_access")


class TabMashupView(C4CSAPTokenLoginMixin, TemplateView):
    template_name = 'c4csap/ticket_tab.html'


class KBHomeView(C4CSAPTokenLoginMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """
        Hide the static tag import to avoid errors with static file
        processors
        """
        url = "/"
        if "q" in self.request.GET and len(self.request.GET["q"])>0:
            query = self.request.GET["q"]
            url = "%s?q=%s" % (
                reverse("search:results", kwargs={"search_model": "documents.Document"}),
                query
            )
        return url


class RedirectToPageView(RedirectView):
    permanent = False

    @method_decorator(public)
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super(RedirectToPageView, self).dispatch(request, *args, **kwargs)

    def get_redirect_host(self, *args, **kwargs):
        host = ""
        if self.request is not None and "system" in self.request.GET:
            host = "https://%s.c4csap.com" % self.request.GET["system"]
        return host


class RedirectToHomeView(RedirectToPageView):

    def get_redirect_url(self, *args, **kwargs):
        """
        Hide the static tag import to avoid errors with static file
        processors
        """
        url = reverse("c4csap:c4csap_kb_home")
        return "%s%s?%s" % (self.get_redirect_host(*args, **kwargs), url, self.request.META["QUERY_STRING"])


class RedirectToServiceTabView(RedirectToPageView):

    def get_redirect_url(self, *args, **kwargs):
        """
        Hide the static tag import to avoid errors with static file
        processors
        """
        url = reverse("c4csap:c4csap_ticket_tab")
        return "%s%s?%s" % (self.get_redirect_host(*args, **kwargs), url, self.request.META["QUERY_STRING"])


class RedirectToServiceItemsView(RedirectToPageView):

    def get_redirect_url(self, *args, **kwargs):
        """
        Hide the static tag import to avoid errors with static file
        processors
        """
        url = reverse("related_c4c_tickets:kb_items")
        return "%s%s?%s" % (self.get_redirect_host(*args, **kwargs), url, self.request.META["QUERY_STRING"])


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
            host, reverse("c4csap:document_version_raw", kwargs={"pk":pk})
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
        redirect_url = reverse("c4csap:document_version_online_viewer", kwargs={"pk":doc.latest_version.id})
        return redirect_url


class DocumentEmbbedView(DocumentPreviewView):
    form_class = DocumentEmbbedViewForm
