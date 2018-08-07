from __future__ import absolute_import, unicode_literals

from django.apps import apps
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from common.classes import DashboardWidget


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


# 重点知识

class TaggedImportantDocumentItems(BaseDetailedWidgetItems):

    def get_queryset(self):
        Tag = apps.get_model(
            app_label='tags', model_name='Tag'
        )
        important = Tag.objects.filter(label='重点知识').last()
        if important is not None:
            return important.documents.defer(
                'description', 'uuid', 'date_added', 'language', 'in_trash',
                'deleted_date_time'
            ).filter(is_stub=False).order_by('-recentdocument__datetime_accessed')
        return self.queryset.none()


detailed_widget_tagged_important_documents = DashboardWidget(
    func=lambda :TaggedImportantDocumentItems().as_string(), icon='fa fa-tags',
    label=_('Tagged Important Documents'),
    link=reverse_lazy(
        'detailed_widgets:redirect_to_important_list',
    )
)