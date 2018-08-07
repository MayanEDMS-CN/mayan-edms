from __future__ import absolute_import, unicode_literals
from django import forms
from documents.forms import DocumentPreviewForm
from .widgets import DocumentEmbbedViewWidget


# Document embbed view forms
class DocumentEmbbedViewForm(DocumentPreviewForm):
    preview = forms.CharField(widget=DocumentEmbbedViewWidget())
