import logging

from cms.models import Page
from django.contrib.contenttypes.models import ContentType
from django.db.models import signals
from django.dispatch import receiver
from django.utils.safestring import mark_safe

from link_all.middleware import Redirect
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
        pages_linked_hrefs = []
        for plugin in link_button_plugins_linked:
            page_url = plugin.page.get_draft_url() if plugin.page.publisher_is_draft else plugin.page.get_public_url()
            link = f"""
                - <a href="{page_url}">{plugin.page.get_title()}</a>
                {'(draft version)' if plugin.page.publisher_is_draft else ''},
                link label - "{plugin.get_link_label()}"
            <br>
            """
            pages_linked_hrefs.append(link)
        pages_linked_urls_str = ''.join(pages_linked_hrefs)
        raise Redirect(
            url_name='admin:cms_page_change',
            error_message=mark_safe(
                f"Cannot delete this page because it's linked "
                f"on the following pages: <br>{pages_linked_urls_str}",
            ),
            args=[instance.get_draft_object().pk],
        )
