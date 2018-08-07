from __future__ import absolute_import, unicode_literals

from django.apps import apps
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView, TemplateView

from documents.views.document_views import DocumentListView
from motd.models import Message


class MessageDisplay(TemplateView):

    template_name = "detailed_widgets/motd_details.html"

    def get_context_data(self, **kwargs):
        context = super(MessageDisplay, self).get_context_data(**kwargs)
        context["title"] = _("Message of Today")
        return context


class MessageDisplayList(MessageDisplay):

    def get_context_data(self, **kwargs):
        context = super(MessageDisplayList, self).get_context_data(**kwargs)
        context["messages"] = Message.objects.get_for_now()
        return context


class MessageDisplayDetail(MessageDisplay):

    def get_context_data(self, **kwargs):
        context = super(MessageDisplayDetail, self).get_context_data(**kwargs)
        pk = kwargs["pk"]
        message = Message.objects.get_for_now().filter(pk=pk).last()
        if message is not None:
            context["messages"] = [message]
        return context


class RecentChangedDocumentListView(DocumentListView):

    def get_document_queryset(self):
        qs = super(RecentChangedDocumentListView, self).get_document_queryset()
        return qs.order_by('-versions__timestamp')

    def get_extra_context(self):
        context = super(RecentChangedDocumentListView, self).get_extra_context()
        context.update(
            {
                'title': _('Recent Changed Documents'),
            }
        )
        return context


class RecentAddedDocumentListView(DocumentListView):

    def get_document_queryset(self):
        qs = super(RecentAddedDocumentListView, self).get_document_queryset()
        return qs.order_by('-date_added')

    def get_extra_context(self):
        context = super(RecentAddedDocumentListView, self).get_extra_context()
        context.update(
            {
                'title': _('Recent Added Documents'),
            }
        )
        return context


class EmptyTaggedImportantDocumentListView(DocumentListView):

    def get_document_queryset(self):
        qs = super(EmptyTaggedImportantDocumentListView, self).get_document_queryset()
        return qs.none()

    def get_extra_context(self):
        context = super(EmptyTaggedImportantDocumentListView, self).get_extra_context()
        context.update(
            {
                'title': _('Tagged Important Documents'),
            }
        )
        return context


class TaggedImportantDocumentRedirect(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        Tag = apps.get_model(
            app_label='tags', model_name='Tag'
        )
        important = Tag.objects.filter(label='重点知识').last()
        if important is not None:
            return reverse_lazy("tags:tag_tagged_item_list", kwargs={"pk":important.id})
        return reverse_lazy("detailed_widgets:empty_important_list")