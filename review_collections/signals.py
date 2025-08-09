from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete

import os

from review_collections.models import Collection


@receiver(pre_save, sender=Collection, dispatch_uid="collection_delete_old_cover_on_update")
def delete_old_cover_on_update(sender, instance, **kwargs):
    if not instance.id:
        return
    old_file = sender.objects.get(id=instance.id).cover
    if os.path.basename(old_file.name) != 'default.jpg':
        old_file.delete(save=False)


@receiver(post_delete, sender=Collection, dispatch_uid="collection_delete_old_cover_on_delete")
def delete_old_cover_on_delete(sender, instance, **kwargs):
    if not instance.id:
        return
    if os.path.basename(instance.cover.name) != 'default.jpg':
        instance.cover.delete(save=False)