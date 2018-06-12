from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView, TemplateView
import logging
from django.template import RequestContext


class TabMashupView(TemplateView):
    template_name = 'appearance/home.html'


class RelatedItemListView(TemplateView):
    template_name = 'c4csap/related_items.html'

    def get_context_data(self, **kwargs):
        data = super(RelatedItemListView, self).get_context_data(**kwargs)
        context = RequestContext(self.request)
        context['request'] = self.request
        data.update({
            'title': _('Setup items'),
        })
        return data


class RedirectToHomeView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """
        Hide the static tag import to avoid errors with static file
        processors
        """
        return '/'