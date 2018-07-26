from __future__ import unicode_literals

from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe


class DocumentEmbbedViewWidget(forms.widgets.Widget):
    """
    Display many small representations of a document pages
    """
    def render(self, name, value, attrs=None):

        output = []
        output.append("""
        <style>
            .well {
                margin-bottom: 0;
                padding-bottom: 0;
            }
            .form-group {
                margin-bottom: 0;
            }
            
        </style>
        """)
        output.append(
            '<div id="carousel-container" class="full-height scrollable" '
            'data-height-difference=20>'
        )
        document = value
        if document.latest_version is not None:
            redirect_url = "%s?embed_mode=1" % reverse("c4csap:document_version_online_viewer", kwargs={"pk": document.latest_version.id})
            output.append(
                "<iframe src=\"" +redirect_url + "\" width=\"100%\" height=\"100%\" frameborder=\"0\"></iframe>"
            )
        output.append('</div>')

        return mark_safe(''.join(output))
