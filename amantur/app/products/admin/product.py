from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.decorators import display

from ..models import Product


@admin.register(Product)
class ProductAdmin(UnfoldModelAdmin):
    compressed_fields = True
    list_display = ('id', 'name', 'price', 'display_categories', 'is_hidden', 'display_photo')
    list_display_links = ('id', 'name')
    list_editable = ('is_hidden',)
    list_filter = ('category', 'is_case')
    search_fields = ('name',)
    autocomplete_fields = ('category',)
    readonly_fields = ('created_at', 'updated_at')

    @display(description=_("Категории"))
    def display_categories(self, obj):
        return ", ".join([cat.name for cat in obj.category.all()])

    @display(description=_("Фото"))
    def display_photo(self, obj):
        if obj.photo:
            return mark_safe(
                f'<img src="{obj.photo.url}" height="120" width="120" '
                f'style="border-radius: 10%;" />')
