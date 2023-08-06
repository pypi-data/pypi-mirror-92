from django.conf.urls import include, url
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.menu import MenuItem
from wagtail.admin.search import SearchArea
from wagtail.admin.site_summary import SummaryItem
from wagtail.core import hooks
from django.utils.html import format_html
from django.templatetags.static import static
from wagtailvideos import urls
from wagtailvideos.forms import GroupVideoPermissionFormSet
from wagtailvideos.models import Video

from .permissions import permission_policy


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^videos/', include(urls)),
    ]


@hooks.register('insert_editor_js')
def editor_js():
    return format_html(
        """
        <script>
            window.chooserUrls.videoChooser = '{0}';
        </script>
        """,
        reverse('wagtailvideos:chooser')
    )


@hooks.register('register_group_permission_panel')
def register_video_permissions_panel():
    return GroupVideoPermissionFormSet


@hooks.register('register_admin_menu_item')
def register_images_menu_item():
    return MenuItem(
        _('Videos'), reverse('wagtailvideos:index'),
        name='videos', classnames='icon icon-media', order=300
    )



class VideoSummaryItem(SummaryItem):
    order = 300
    template = "wagtailvideos/homepage/videos_summary.html"

    def get_context(self):
        return {
            "total_videos": Video.objects.count(),
        }

    def is_shown(self):
        return permission_policy.user_has_any_permission(
            self.request.user, ["add", "change", "delete"]
        )


@hooks.register("construct_homepage_summary_items")
def add_media_summary_item(request, items):
    items.append(VideoSummaryItem(request))


class VideoSearchArea(SearchArea):
    def is_shown(self, request):
        return permission_policy.user_has_any_permission(
            request.user, ["add", "change", "delete"]
        )


@hooks.register("register_admin_search_area")
def register_media_search_area():
    return VideoSearchArea(
        _("Video"),
        reverse("wagtailvideos:index"),
        name="video",
        classnames="icon icon-media",
        order=400,
    )

@hooks.register('insert_global_admin_css')
def summary_css():
    return format_html('<link rel="stylesheet" href="{}">', static('wagtailvideos/css/summary-override.css'))
