from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.apps import apps

from navigation import Link

def is_tag_displayed(context):
    DashboardDisplayedTag = apps.get_model(
        app_label="detailed_widgets",
        model_name="DashboardDisplayedTag"
    )
    return DashboardDisplayedTag.objects.is_tag_displayed(context["object"])


link_dashboard_remove_tag = Link(
    args='resolved_object.id',
    condition=is_tag_displayed,
    text=_('Remove From Dashboard'), view='detailed_widgets:dashboard_remove_tag'
)

link_dashboard_add_tag = Link(
    args='resolved_object.id',
    condition=lambda context: not is_tag_displayed(context),
    text=_('Add To Dashboard'), view='detailed_widgets:dashboard_add_tag'
)
