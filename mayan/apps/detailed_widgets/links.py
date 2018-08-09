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


def is_document_favourite(context):
    user = context["user"]
    document = context["object"]
    FavouriteDocument = apps.get_model(
        app_label="detailed_widgets",
        model_name="FavouriteDocument"
    )
    return FavouriteDocument.objects.is_users_favourite(user, document)


link_document_remove_favourite = Link(
    args='resolved_object.id',
    condition=is_document_favourite,
    text=_('Remove From My Favourites'), view='detailed_widgets:document_remove_favourite'
)

link_document_add_favourite = Link(
    args='resolved_object.id',
    condition=lambda context: not is_document_favourite(context),
    text=_('Add To My Favourites'), view='detailed_widgets:document_add_favourite'
)

link_my_favourite_documents = Link(
    icon='fa fa-star-o',
    text=_("My Favourites"), view="detailed_widgets:favourite_document_list"
)
