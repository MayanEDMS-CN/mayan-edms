from __future__ import absolute_import, unicode_literals

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, RedirectView
from django.utils.translation import ugettext_lazy as _

from c4csap.views import C4CSAPTokenLoginMixin
from common.generics import SingleObjectEditView, SingleObjectCreateView, SingleObjectListView, ConfirmView
from common.utils import resolve
from documents.models import Document
from .models import C4CServiceTicket, DocumentServiceTicketRelatedSettings



class DocumentCreateRelationRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs["pk"]
        ticketid = self.request.session.get("ticketid", None)
        if ticketid is None:
            return reverse_lazy('related_c4c_tickets:relation_create', kwargs={"pk":pk})
        ticket, created = C4CServiceTicket.objects.get_or_create(ticket_id=ticketid)
        relation, created = DocumentServiceTicketRelatedSettings.objects.get_or_create(
            ticket_id=ticket.id,
            document_id=pk
        )
        return reverse("related_c4c_tickets:relation_edit", kwargs={"pk":relation.id})


class C4CTicketRelationCreateView(SingleObjectCreateView):
    extra_context = {'title': _('Create C4C Ticket Relation')}
    fields = ('ticket_id',)
    model = C4CServiceTicket

    def post(self, request, *args, **kwargs):
        """
        重载post，处理 ticket_id 已存在的情况
        """
        form = self.get_form()
        if form.is_valid():
            return super(C4CTicketRelationCreateView, self).post(request, *args, **kwargs)
        else:
            bd_field = form.fields["ticket_id"].get_bound_field(form, "ticket_id")
            c4c_ticket_id = bd_field.value()
            ticket = C4CServiceTicket.objects.filter(ticket_id=c4c_ticket_id).last()
            if ticket is not None:          # 已存在
                self.object = ticket
                document_id = self.kwargs["pk"]
                relation, created = DocumentServiceTicketRelatedSettings.objects.get_or_create(
                    document_id=document_id, ticket_id=self.object.id)      # 找到它与当前工单的关系
                if relation.related == False:       # 设成相关
                    relation.related = True
                    relation.save()
                return HttpResponseRedirect(self.get_success_url())

        return super(C4CTicketRelationCreateView, self).post(request, *args, **kwargs)


    def get_post_action_redirect(self):
        document_id = self.kwargs["pk"]
        return reverse_lazy('related_c4c_tickets:document_relation_list', kwargs={"pk":document_id})


class C4CTicketDeleteConfirmView(ConfirmView):
    extra_context = {
        'title': _('Delete the selected C4C Ticket Relation?')
    }

    def object_action(self, instance):
        instance.delete()

    def view_action(self):
        instance = get_object_or_404(DocumentServiceTicketRelatedSettings, pk=self.kwargs['pk'])
        document_title = "%s" % instance.document
        ticket_id = instance.ticket.ticket_id
        self.object_action(instance=instance)
        messages.success(
            self.request, _('Relation between: %(document)s and C4C ticket %(ticket_id)s deleted.') % {
                'document': document_title, 'ticket_id': ticket_id
            }
        )


class C4CTicketRelationEditView(SingleObjectEditView):
    fields = ('related',)

    def get_object(self, queryset=None):
        pk = self.kwargs["pk"]
        obj = DocumentServiceTicketRelatedSettings.objects.get(pk=pk)
        return obj

    def get_extra_context(self):
        return {
            'title': _(
                'Edit relationship for document : %s'
            ) % self.get_object().document
        }


class C4CTicketRelationListView(SingleObjectListView):
    extra_context = {
        'title': _('Related C4C Tickets'),
    }

    def get_object_list(self):
        pk = self.kwargs["pk"]
        doc = Document.objects.get(pk=pk)
        return doc.ticket_relationships.filter(related=True).all()


class RelatedItemListView(C4CSAPTokenLoginMixin, TemplateView):
    template_name = 'c4csap/related_items.html'

    def get_context_data(self, **kwargs):
        data = super(RelatedItemListView, self).get_context_data(**kwargs)
        context = RequestContext(self.request)
        context['request'] = self.request
        ticket_id = self.request.session.get("ticketid", None)
        if ticket_id is not None:
            ticket, created = C4CServiceTicket.objects.get_or_create(ticket_id=ticket_id)
            data.update({
                "relationships": ticket.document_relationships.filter(related=True).all()
            })
        data.update({
            'title': _('Setup items'),
        })
        return data
