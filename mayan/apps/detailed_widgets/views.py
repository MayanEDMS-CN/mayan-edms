from __future__ import absolute_import, unicode_literals

from django.apps import apps
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView, TemplateView
from django.contrib import messages

from acls.models import AccessControlList
from common.generics import ConfirmView
from documents.models import Document
from documents.permissions import permission_document_view
from documents.views.document_views import DocumentListView
from motd.models import Message
from tags.models import Tag as DocumentTag

from .models import DashboardDisplayedTag, FavouriteDocument
from .dashboard_widgets import add_tag_to_dashboard, remove_tag_from_dashboard


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


class EmptyTaggedDocumentListDashboardView(DocumentListView):

    def get_document_queryset(self):
        qs = super(EmptyTaggedDocumentListDashboardView, self).get_document_queryset()
        return qs.none()

    def get_extra_context(self):
        context = super(EmptyTaggedDocumentListDashboardView, self).get_extra_context()
        Tag = apps.get_model(
            app_label='tags', model_name='Tag'
        )
        pk = self.kwargs["pk"]
        tag = Tag.objects.filter(pk=pk).last()

        if tag is not None:
            context.update(
                {
                    'title': _('Tagged %(tag)s Documents') % tag,
                }
            )
        return context


class TaggedDocumentDashboardRedirect(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        Tag = apps.get_model(
            app_label='tags', model_name='Tag'
        )
        pk = kwargs["pk"]
        tag = Tag.objects.filter(pk=pk).last()
        if tag is not None:
            return reverse_lazy("tags:tag_tagged_item_list", kwargs={"pk":pk})
        return reverse_lazy("detailed_widgets:empty_tagged_list", kwargs={"pk":pk})


class DashboardDisplayedTagRemoveConfirmView(ConfirmView):

    extra_context = {
        'title': _('Remove the selected Tag\'s documents from the dashboard?')
    }

    def object_action(self, instance):
        DashboardDisplayedTag.objects.remove_tag(instance)
        remove_tag_from_dashboard(instance)

    def view_action(self):
        instance = get_object_or_404(DocumentTag, pk=self.kwargs['pk'])
        if DashboardDisplayedTag.objects.is_tag_displayed(instance):
            self.object_action(instance=instance)
            messages.success(
                self.request, _('Tag %(tag)s \'s documents are successfully removed from the dashboard.') % {
                    'tag': instance
                }
            )
        else:
            messages.error(
                self.request, _("Tag %(tag)s\'s documents are not on the dashboard.") % {
                    'tag': instance
                }
            )



class DashboardDisplayedTagAddConfirmView(ConfirmView):

    extra_context = {
        'title': _('Add the selected Tag\'s documents to the dashboard?')
    }

    def object_action(self, instance):
        DashboardDisplayedTag.objects.add_tag(instance)
        add_tag_to_dashboard(instance)

    def view_action(self):
        instance = get_object_or_404(DocumentTag, pk=self.kwargs['pk'])
        if DashboardDisplayedTag.objects.is_tag_displayed(instance):
            messages.error(
                self.request, _("Tag %(tag)s\'s documents are already added to the dashboard.") % {
                    'tag': instance
                }
            )
        else:
            self.object_action(instance=instance)
            messages.success(
                self.request, _('Tag %(tag)s \'s documents are successfully added to the dashboard.') % {
                    'tag': instance
                }
            )


class FavouriteDocumentRemoveConfirmView(ConfirmView):

    extra_context = {
        'title': _('Remove the selected document from your favourites?')
    }

    def object_action(self, instance):
        FavouriteDocument.objects.remove_users_favourite(self.request.user, instance)

    def view_action(self):
        instance = get_object_or_404(Document, pk=self.kwargs['pk'])
        if FavouriteDocument.objects.is_users_favourite(self.request.user, instance) :
            self.object_action(instance=instance)
            messages.success(
                self.request, _('%(document)s is successfully removed from your favourites.') % {
                    'document': instance
                }
            )
        else:
            messages.error(
                self.request, _("%(document)s is not in your favourites.") % {
                    'document': instance
                }
            )


class FavouriteDocumentAddConfirmView(ConfirmView):

    extra_context = {
        'title': _('Add the selected document to your favourites?')
    }

    def object_action(self, instance):
        source_document = get_object_or_404(
            Document.passthrough, pk=instance.pk
        )

        AccessControlList.objects.check_access(
            permissions=permission_document_view, user=self.request.user,
            obj=source_document
        )
        FavouriteDocument.objects.add_users_favourite(self.request.user, instance)

    def view_action(self):
        instance = get_object_or_404(Document, pk=self.kwargs['pk'])
        if FavouriteDocument.objects.is_users_favourite(self.request.user, instance):
            messages.error(
                self.request, _("%(document)s is already your favourite.") % {
                    'document': instance
                }
            )
        else:
            self.object_action(instance=instance)
            messages.success(
                self.request, _('%(document)s is successfully added to your favourite.') % {
                    'document': instance
                }
            )


class FavouriteDocumentListView(DocumentListView):

    def get_document_queryset(self):
        qs = super(FavouriteDocumentListView, self).get_document_queryset().filter(favouritees__user=self.request.user)
        return qs.order_by('-favouritees__added_datetime')

    def get_extra_context(self):
        context = super(FavouriteDocumentListView, self).get_extra_context()
        context.update(
            {
                'title': _('My Favourite Documents'),
            }
        )
        return context
