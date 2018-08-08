from __future__ import unicode_literals


from documents.widgets import DocumentThumbnailWidget


class DocumentThumbnailWithPagesPreviewWidget(DocumentThumbnailWidget):

    fancybox_class = "open_fancybox"
    click_view_name = "preview_pages:page_images_json"
    click_view_query_dict = {}

    def get_click_view_kwargs(self, instance):
        return {"pk": instance.pk}