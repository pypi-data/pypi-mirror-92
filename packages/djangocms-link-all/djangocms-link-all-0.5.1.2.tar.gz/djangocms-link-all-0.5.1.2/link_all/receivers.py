import logging

from cms.models import Page
from django.contrib.contenttypes.models import ContentType
from django.db.models import ProtectedError, signals
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from link_all.models import LinkButtonPluginModel


logger = logging.getLogger(__name__)


@receiver(signals.pre_delete, sender=Page, dispatch_uid='protect_linked_pages_from_deletion')
def protect_linked_pages_from_deletion(sender, instance: Page, **kwargs):
    link_button_plugins_linked = LinkButtonPluginModel.objects.filter(
        link_content_type=ContentType.objects.get_for_model(instance),
        link_instance_pk=instance.pk,
    )
    is_page_linked = link_button_plugins_linked.exists()
    if is_page_linked:
        pages_linked_urls = [plugin.link_instance.get_absolute_url() for plugin in link_button_plugins_linked]
        pages_linked_urls_str = '\n'.join(pages_linked_urls)
        logger.error(f"the following pages now contains an empty link plugin - {pages_linked_urls_str}")
        # raise ProtectedError(
        #     mark_safe(
        #         f"Cannot delete this page because it's linked on the following pages: {pages_linked_urls_str}",
        #     ),
        #     protected_objects=[],
        # )
