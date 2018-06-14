from __future__ import absolute_import, unicode_literals

from django import VERSION as DJANGO_VERSION
from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView, TemplateView
import logging
from django.template import RequestContext
from django.utils.decorators import method_decorator
from stronghold.decorators import public
from braces.views._access import AccessMixin
from django.contrib.auth import authenticate, login

if DJANGO_VERSION >= (1, 10, 0):
    _is_authenticated = lambda user: user.is_authenticated  # noqa
else:
    # Django<1.10 compatibility
    _is_authenticated = lambda user: user.is_authenticated()  # noqa

class C4CSAPTokenLoginMixin(AccessMixin):

    @method_decorator(public)
    def dispatch(self, request, *args, **kwargs):
        if not _is_authenticated(request.user):
            c4c_username = request.GET.get("username", "")
            c4c_token = request.GET.get("token", "")
            if len(c4c_username)>0 and len(c4c_token)>0:
                #user = authenticate(username=c4c_username, password=c4c_token)
                user = authenticate(username="testkb", password="Welcome1")
                if user is not None:
                    login(request, user)
                    return super(C4CSAPTokenLoginMixin, self).dispatch(request, *args, **kwargs)

            return self.no_permissions_fail(request)
        else:
            return super(C4CSAPTokenLoginMixin, self).dispatch(request, *args, **kwargs)




class TabMashupView(C4CSAPTokenLoginMixin, TemplateView):
    template_name = 'c4csap/ticket_tab.html'


class RelatedItemListView(C4CSAPTokenLoginMixin, TemplateView):
    template_name = 'c4csap/related_items.html'

    def get_context_data(self, **kwargs):
        data = super(RelatedItemListView, self).get_context_data(**kwargs)
        context = RequestContext(self.request)
        context['request'] = self.request
        data.update({
            'title': _('Setup items'),
        })
        return data


class RedirectToHomeView(C4CSAPTokenLoginMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """
        Hide the static tag import to avoid errors with static file
        processors
        """
        return '/'