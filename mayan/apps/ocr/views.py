from __future__ import absolute_import

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessEntry
from common.utils import encapsulate
from documents.models import Document
from documents.widgets import document_link, document_thumbnail
from permissions.models import Permission

from .api import clean_pages
from .exceptions import ReQueueError
from .models import DocumentQueue, QueueDocument
from .permissions import (PERMISSION_OCR_CLEAN_ALL_PAGES,
                          PERMISSION_OCR_DOCUMENT,
                          PERMISSION_OCR_DOCUMENT_DELETE)
from .tasks import task_do_ocr


def queue_document_list(request, queue_name='default'):
    Permission.objects.check_permissions(request.user, [PERMISSION_OCR_DOCUMENT])

    document_queue = get_object_or_404(DocumentQueue, name=queue_name)

    context = {
        'object_list': document_queue.documents.all(),
        'title': _(u'Documents in queue: %s') % document_queue,
        'hide_object': True,
        'queue': document_queue,
        'object_name': _(u'Document queue'),
        'navigation_object_name': 'queue',
        'list_object_variable_name': 'queue_document',
        'extra_columns': [
            {'name': _('Document'), 'attribute': encapsulate(lambda x: document_link(x.document) if hasattr(x, 'document') else _(u'Missing document.'))},
            {'name': _(u'Thumbnail'), 'attribute': encapsulate(lambda x: document_thumbnail(x.document))},
            {'name': _('Added'), 'attribute': encapsulate(lambda x: unicode(x.datetime_submitted).split('.')[0]), 'keep_together':True},
            {'name': _('Node'), 'attribute': 'node_name'},
            {'name': _('Result'), 'attribute': 'result'},
        ],
        'multi_select_as_buttons': True,
    }

    return render_to_response('main/generic_list.html', context,
        context_instance=RequestContext(request))


def queue_document_delete(request, queue_document_id=None, queue_document_id_list=None):
    Permission.objects.check_permissions(request.user, [PERMISSION_OCR_DOCUMENT_DELETE])

    if queue_document_id:
        queue_documents = [get_object_or_404(QueueDocument, pk=queue_document_id)]
    elif queue_document_id_list:
        queue_documents = [get_object_or_404(QueueDocument, pk=queue_document_id) for queue_document_id in queue_document_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one queue document.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    if request.method == 'POST':
        for queue_document in queue_documents:
            try:
                queue_document.delete()
                messages.success(request, _(u'Queue document: %(document)s deleted successfully.') % {
                    'document': queue_document.document})

            except Exception as exception:
                messages.error(request, _(u'Error deleting document: %(document)s; %(error)s') % {
                    'document': queue_document, 'error': exception})
        return HttpResponseRedirect(next)

    context = {
        'next': next,
        'previous': previous,
        'delete_view': True,
        'form_icon': u'hourglass_delete.png',
    }

    if len(queue_documents) == 1:
        context['object'] = queue_documents[0]
        context['title'] = _(u'Are you sure you wish to delete queue document: %s?') % ', '.join([unicode(d) for d in queue_documents])
    elif len(queue_documents) > 1:
        context['title'] = _(u'Are you sure you wish to delete queue documents: %s?') % ', '.join([unicode(d) for d in queue_documents])

    return render_to_response('main/generic_confirm.html', context,
        context_instance=RequestContext(request))


def queue_document_multiple_delete(request):
    return queue_document_delete(request, queue_document_id_list=request.GET.get('id_list', ''))


def submit_document_multiple(request):
    for item_id in request.GET.get('id_list', '').split(','):
        submit_document(request, item_id)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def submit_document(request, document_id):
    document = get_object_or_404(Document, pk=document_id)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_OCR_DOCUMENT])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_OCR_DOCUMENT, request.user, document)

    return submit_document_to_queue(request, document=document,
        post_submit_redirect=request.META.get('HTTP_REFERER', '/'))


def submit_document_to_queue(request, document, post_submit_redirect=None):
    """
    This view is meant to be reusable
    """

    task_do_ocr.delay(document.pk)
    messages.success(request, _(u'Document: %(document)s was added to the OCR queue.') % {
        'document': document}
    )

    if post_submit_redirect:
        return HttpResponseRedirect(post_submit_redirect)


def re_queue_document(request, queue_document_id=None, queue_document_id_list=None):
    Permission.objects.check_permissions(request.user, [PERMISSION_OCR_DOCUMENT])

    if queue_document_id:
        queue_documents = [get_object_or_404(QueueDocument, pk=queue_document_id)]
    elif queue_document_id_list:
        queue_documents = [get_object_or_404(QueueDocument, pk=queue_document_id) for queue_document_id in queue_document_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one queue document.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    if request.method == 'POST':
        for queue_document in queue_documents:
            try:
                queue_document.requeue()
                messages.success(
                    request,
                    _(u'Document: %(document)s was re-queued to the OCR queue: %(queue)s') % {
                        'document': queue_document.document,
                        'queue': queue_document.document_queue.label
                    }
                )
            except Document.DoesNotExist:
                messages.error(request, _(u'Document id#: %d, no longer exists.') % queue_document.document_id)
            except ReQueueError:
                messages.warning(
                    request,
                    _(u'Document: %s is already being processed and can\'t be re-queded.') % queue_document
                )
        return HttpResponseRedirect(next)

    context = {
        'next': next,
        'previous': previous,
        'form_icon': u'hourglass_add.png',
    }

    if len(queue_documents) == 1:
        context['object'] = queue_documents[0]
        context['title'] = _(u'Are you sure you wish to re-queue document: %s?') % ', '.join([unicode(d) for d in queue_documents])
    elif len(queue_documents) > 1:
        context['title'] = _(u'Are you sure you wish to re-queue documents: %s?') % ', '.join([unicode(d) for d in queue_documents])

    return render_to_response('main/generic_confirm.html', context,
        context_instance=RequestContext(request))


def re_queue_multiple_document(request):
    return re_queue_document(request, queue_document_id_list=request.GET.get('id_list', []))


def all_document_ocr_cleanup(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_OCR_CLEAN_ALL_PAGES])

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))

    if request.method != 'POST':
        return render_to_response('main/generic_confirm.html', {
            'previous': previous,
            'next': next,
            'title': _(u'Are you sure you wish to clean up all the pages content?'),
            'message': _(u'On large databases this operation may take some time to execute.'),
            'form_icon': u'text_strikethroungh.png',
        }, context_instance=RequestContext(request))
    else:
        try:
            clean_pages()
            messages.success(request, _(u'Document pages content clean up complete.'))
        except Exception as exception:
            messages.error(request, _(u'Document pages content clean up error: %s') % exception)

        return HttpResponseRedirect(next)


def display_link(obj):
    output = []
    if hasattr(obj, 'get_absolute_url'):
        output.append(u'<a href="%(url)s">%(obj)s</a>' % {
            'url': obj.get_absolute_url(),
            'obj': obj
        })
    if output:
        return u''.join(output)
    else:
        return obj
