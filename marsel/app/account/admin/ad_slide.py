from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.decorators import display

from account.models import AdSlide


@admin.register(AdSlide)
class AdSlideAdmin(UnfoldModelAdmin):
    list_display = ('title', 'display_photo')

    @display(description=_("Фото"))
    def display_photo(self, obj):
        if obj.photo:
            return mark_safe(
                f'<img src="{obj.photo.url}" height="auto" width="120" '
                f'style="border-radius: 10%;" />')