from __future__ import unicode_literals

from django.db import models


class DashboardDisplayedTagManager(models.Manager):

    def is_tag_displayed(self, tag):
        ins = self.model.objects.filter(tag=tag).last()
        return ins is not None

    def add_tag(self, tag):
        ins = self.model.objects.filter(tag=tag).last()
        if ins is None:
            self.model.objects.create(tag=tag)

    def remove_tag(self, tag):
        ins = self.model.objects.filter(tag=tag).last()
        if ins is not None:
            ins.delete()


class FavouriteDocumentManager(models.Manager):

    def is_users_favourite(self, user, document):
        num  = self.model.objects.filter(
            user=user, document=document
        ).count()
        return num > 0

    def add_users_favourite(self, user, document):
        if not self.is_users_favourite(user, document):
            self.model.objects.create(
                user=user, document=document
            )

    def remove_users_favourite(self, user, document):
        fav = self.model.objects.filter(user=user, document=document).last()
        if fav is not None:
            fav.delete()

