from __future__ import unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from acls import ModelPermission
from acls.permissions import permission_acl_edit, permission_acl_view
from common import (
    MayanAppConfig, menu_facet, menu_main, menu_multi_item, menu_object,
    menu_sidebar, menu_secondary
)
from .links import link_document_online_viewer, link_document_version_online_viewer, \
    link_document_c4c_relationship_settings
from document_parsing.parsers import Parser, PopplerParser
from converter.classes import CONVERTER_OFFICE_FILE_MIMETYPES

class C4CSapApp(MayanAppConfig):
    has_tests = True
    name = 'c4csap'
    verbose_name = _('C4C SAP')

    def ready(self):

        super(C4CSapApp, self).ready()

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        DocumentVersion = apps.get_model(
            app_label='documents', model_name='DocumentVersion'
        )

        menu_object.bind_links(
            links=(link_document_online_viewer,), sources=(Document,)
        )

        menu_object.bind_links(
            links=(link_document_version_online_viewer,), sources=(DocumentVersion,)
        )

        menu_object.bind_links(
            links=(link_document_c4c_relationship_settings,), sources=(Document,)
        )

        menu_facet.bind_links(
            links=(link_document_online_viewer,), sources=(Document,)
        )

        menu_facet.bind_links(
            links=(link_document_version_online_viewer,), sources=(DocumentVersion,)
        )

        Parser.register(CONVERTER_OFFICE_FILE_MIMETYPES, (PopplerParser,))