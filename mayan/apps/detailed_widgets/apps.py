from __future__ import unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from acls import ModelPermission
from acls.permissions import permission_acl_edit, permission_acl_view
from common import (
    MayanAppConfig, menu_facet, menu_main, menu_multi_item, menu_object,
    menu_sidebar, menu_secondary
)
from common.dashboards import dashboard_main
from documents.dashboard_widgets import widget_document_types, widget_documents_in_trash, \
    widget_new_documents_this_month, widget_pages_per_month, widget_total_documents
from checkouts.dashboard_widgets import widget_checkouts
from .dashboard_widgets import detailed_widget_total_documents, detailed_widget_recent_changed_documents, \
    detailed_widget_checkout_documents, detailed_widget_recent_added_documents, \
    detailed_widget_recent_viewed_documents, detailed_widget_tagged_important_documents, \
    detailed_widget_message_of_today


class DetailedWidgetApp(MayanAppConfig):
    has_tests = True
    name = 'detailed_widgets'
    verbose_name = _('Detailed Widget')

    def ready(self):

        super(DetailedWidgetApp, self).ready()

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        dashboard_main.remove_widget(widget_total_documents)
        dashboard_main.remove_widget(widget_pages_per_month)
        dashboard_main.remove_widget(widget_new_documents_this_month)
        dashboard_main.remove_widget(widget_documents_in_trash)
        dashboard_main.remove_widget(widget_document_types)
        dashboard_main.remove_widget(widget_checkouts)

        dashboard_main.add_widget(detailed_widget_recent_added_documents)
        dashboard_main.add_widget(detailed_widget_recent_viewed_documents)
        dashboard_main.add_widget(detailed_widget_recent_changed_documents)
        dashboard_main.add_widget(detailed_widget_tagged_important_documents)
        dashboard_main.add_widget(detailed_widget_message_of_today)
