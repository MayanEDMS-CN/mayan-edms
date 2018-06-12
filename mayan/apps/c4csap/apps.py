from __future__ import unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from acls import ModelPermission
from acls.permissions import permission_acl_edit, permission_acl_view
from common import (
    MayanAppConfig, menu_facet, menu_main, menu_multi_item, menu_object,
    menu_sidebar
)


class C4CSapApp(MayanAppConfig):
    has_tests = True
    name = 'c4csap'
    verbose_name = _('C4C SAP')

    def ready(self):
        super(C4CSapApp, self).ready()