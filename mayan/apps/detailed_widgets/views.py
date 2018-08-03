from __future__ import absolute_import, unicode_literals

from django.apps import apps
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView

from documents.views.document_views import DocumentListView


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