from __future__ import unicode_literals

from django.template import Library

from ..dashboard_widgets import my_favourite_documents

register = Library()


@register.simple_tag(takes_context=True)
def user_favourites_items(context):
    return my_favourite_documents(context)
