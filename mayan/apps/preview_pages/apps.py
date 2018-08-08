from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from common import MayanAppConfig

class PreviewPagesApp(MayanAppConfig):
    has_tests = False
    name = "preview_pages"
    verbose_name = _('Preview With Pages')

    def ready(self):

        super(PreviewPagesApp, self).ready()