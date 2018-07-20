from __future__ import unicode_literals

from django.contrib import admin
from .models import (
    C4CServiceTicket,
    DocumentServiceTicketRelatedSettings,
)


class RelateddocumentInline(admin.StackedInline):
    model = DocumentServiceTicketRelatedSettings
    classes = ('collapse-open',)


@admin.register(C4CServiceTicket)
class C4CTicketAdmin(admin.ModelAdmin):
    inlines = (RelateddocumentInline,)
