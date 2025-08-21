from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete

import os

from reviews.models import Review


@receiver(pre_save, sender=Review, dispatch_uid="review_delete_old_cover_on_update")
def delete_old_cover_on_update(sender, instance, **kwargs):
    if not instance.id:
        return
    old_file = sender.objects.get(id=instance.id).cover
    if os.path.basename(old_file.name) != 'default.jpg':
        if instance.cover != old_file:
            old_file.delete(save=False)


@receiver(post_delete, sender=Review, dispatch_uid="review_delete_old_cover_on_delete")
def delete_old_cover_on_delete(sender, instance, **kwargs):
    if not instance.id:
        return
    if os.path.basename(instance.cover.name) != 'default.jpg':
        instance.cover.delete(save=False)
