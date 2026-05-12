from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.decorators import display

from .models import Hit


@admin.register(Hit)
class HitAdmin(UnfoldModelAdmin):
    compressed_fields = True
    list_display = ('id', 'short_text', 'order', 'is_hidden', 'display_photo')
    list_display_links = ('id', 'short_text')
    list_editable = ('order', 'is_hidden')
    ordering = ('order',)

    @display(description=_("Текст"))
    def short_text(self, obj):
        return obj.text[:60] + '…' if len(obj.text) > 60 else obj.text

    @display(description=_("Фото"))
    def display_photo(self, obj):
        if obj.photo:
            return mark_safe(
                f'<img src="{obj.photo.url}" height="80" width="80" '
                f'style="border-radius: 8px; object-fit: cover;" />')
