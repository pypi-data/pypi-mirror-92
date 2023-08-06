from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel

from wagtailvideos.edit_handlers import VideoChooserPanel
from wagtailvideos.blocks import VideoChooserBlock

class TestPage(Page):
    video_field = models.ForeignKey(
        'wagtailvideos.Video', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)

    video_streamfield = StreamField([
        ('video', VideoChooserBlock())
    ], blank=True)

    content_panels = Page.content_panels + [
        VideoChooserPanel('video_field'),
        StreamFieldPanel('video_streamfield'),
    ]
