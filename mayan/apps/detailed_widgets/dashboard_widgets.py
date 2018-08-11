from __future__ import absolute_import, unicode_literals

import logging
import json

from django.apps import apps
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from common.classes import DashboardWidget
from common.dashboards import dashboard_main


logger = logging.getLogger(__file__)


class BaseDetailedWidgetItems(object):

    template_name = "detailed_widgets/detailed_dashboard_widget_items.html"

    def __init__(self, queryset=None, template_name=None):
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        if template_name is not None:
            self.template_name = template_name

        if queryset is None:
            self.queryset = Document.objects.defer(
                'description', 'uuid', 'date_added', 'language', 'in_trash',
                'deleted_date_time'
            ).filter(is_stub=False)
        else:
            self.queryset = queryset

    def get_queryset(self):
        return self.queryset

    def as_string(self):
        return render_to_string(self.template_name,
                                context={
                                    "documents": self.get_queryset()[:10]
                                })

# 所有知识

class AllDocumentsItems(BaseDetailedWidgetItems):
    pass


detailed_widget_total_documents = DashboardWidget(
    icon='fa fa-file', func=lambda: AllDocumentsItems().as_string(),
    label=_('Total documents'),
    link=reverse_lazy('documents:document_list')
)


# 最近版本更新过的知识

class RecentChangedDocumentItems(BaseDetailedWidgetItems):

    def get_queryset(self):
        return self.queryset.order_by('-versions__timestamp')


detailed_widget_recent_changed_documents = DashboardWidget(
    func=lambda :RecentChangedDocumentItems(
            template_name="detailed_widgets/detailed_dashboard_widget_items_version_updated.html"
        ).as_string(), icon='fa fa-edit',
    label=_('Recent Changed Documents'),
    link=reverse_lazy(
        'detailed_widgets:recent_changed_list',
    )
)


# 最近新增的知识

class RecentAddedDocumentItems(BaseDetailedWidgetItems):

    def get_queryset(self):
        return self.queryset.order_by('-date_added')


detailed_widget_recent_added_documents = DashboardWidget(
    func=lambda :RecentAddedDocumentItems(
            template_name="detailed_widgets/detailed_dashboard_widget_items_date_added.html"
        ).as_string(), icon='fa fa-file-o',
    label=_('Recent Added Documents'),
    link=reverse_lazy(
        'detailed_widgets:recent_added_list',
    )
)


# 最近看过的知识

class RecentViewedDocumentItems(BaseDetailedWidgetItems):

    def get_queryset(self):
        return self.queryset.order_by('-recentdocument__datetime_accessed')


detailed_widget_recent_viewed_documents = DashboardWidget(
    func=lambda :RecentViewedDocumentItems(
            template_name="detailed_widgets/detailed_dashboard_widget_items_recent_viewed.html"
        ).as_string(), icon='fa fa-eye',
    label=_('Recent Viewed Documents'),
    link=reverse_lazy(
        'documents:document_list_recent',
    )
)


# 检出的知识

class CheckoutDocumentItems(BaseDetailedWidgetItems):

    def get_queryset(self):
        DocumentCheckout = apps.get_model(
            app_label='checkouts', model_name='DocumentCheckout'
        )
        return self.queryset.filter(
            pk__in=DocumentCheckout.objects.all().values_list(
                'document__pk', flat=True
            )
        )

detailed_widget_checkout_documents = DashboardWidget(
    func=lambda :CheckoutDocumentItems().as_string(), icon='fa fa-shopping-cart',
    label=_('Checkout Documents'),
    link=reverse_lazy(
        'checkouts:checkout_list',
    )
)


# 今日消息

class MessageOfTodayItems(BaseDetailedWidgetItems):

    def get_queryset(self):
        Message = apps.get_model(
            app_label='motd', model_name='Message'
        )
        return Message.objects.get_for_now()


detailed_widget_message_of_today = DashboardWidget(
    func=lambda: MessageOfTodayItems(
            template_name="detailed_widgets/detailed_dashboard_widget_motd.html"
        ).as_string(),
    icon='fa fa-bell-o',
    label=_('Message of Today'),
    link=reverse_lazy(
        'detailed_widgets:motd_list',
    )
)

# 打标签的知识

class TaggedDocumentDashboardItems(BaseDetailedWidgetItems):

    def __init__(self, tag, *args, **kwargs):
        super(TaggedDocumentDashboardItems, self).__init__(*args, **kwargs)
        self.tag = tag

    def get_queryset(self):
        if self.tag is not None:
            return self.tag.documents.defer(
                'description', 'uuid', 'language', 'in_trash',
                'deleted_date_time'
            ).filter(is_stub=False).order_by('-date_added')
        return self.queryset.none()


def add_tag_to_dashboard(tag, order=0):
    dashboard_main.add_widget(DashboardWidget(
        func=lambda: TaggedDocumentDashboardItems(tag).as_string(), icon='fa fa-tags',
        label="%s" % tag,
        link=reverse_lazy(
            'detailed_widgets:redirect_to_tagged_list', kwargs={"pk": tag.id}
        )
    ), order=order)

def remove_tag_from_dashboard(tag):
    for widget in list(dashboard_main.widgets.keys()):
        if widget.label == "%s" % tag:
            del dashboard_main.widgets[widget]


# 我的收藏
# 因为 widget 无法获取 context["user"]， 所以，必须
# 配合 templatetags.detailed_widgets_tags.user_favourites_items 使用
# 还要改 templates

class FavouriteDocumentDashboardItems(BaseDetailedWidgetItems):

    def __init__(self, user, *args, **kwargs):
        super(FavouriteDocumentDashboardItems, self).__init__(*args, **kwargs)
        self.user = user

    def get_queryset(self):
        qs = super(FavouriteDocumentDashboardItems, self).get_queryset()
        return qs.filter(favouritees__user=self.user).order_by("-favouritees__added_datetime")


def my_favourite_documents(context):
    user = context["user"]
    return FavouriteDocumentDashboardItems(
            user,
            template_name="detailed_widgets/detailed_dashboard_widget_items_favourite_added.html"
        ).as_string()


detailed_widget_favourite_document = DashboardWidget(
    func = lambda : "user_favourites_items",
    label = _("My Favourite"), icon='fa fa-star-o',
    link=reverse_lazy(
        "detailed_widgets:favourite_document_list"
    )
)
