from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin as UnfoldModelAdmin, TabularInline
from unfold.decorators import display

from ..models import Product, ProductPhoto


class ProductPhotoInline(TabularInline):
    model = ProductPhoto
    extra = 1
    fields = ('photo', 'order', 'display_preview')
    readonly_fields = ('display_preview',)

    @display(description=_("Превью"))
    def display_preview(self, obj):
        if obj.photo:
            return mark_safe(
                f'<img src="{obj.photo.url}" height="80" width="80" '
                f'style="border-radius: 8px; object-fit: cover;" />')
        return "—"


@admin.register(Product)
class ProductAdmin(UnfoldModelAdmin):
    compressed_fields = True
    list_display = ('id', 'name', 'price', 'display_categories', 'is_hidden', 'display_photo')
    list_display_links = ('id', 'name')
    list_editable = ('is_hidden',)
    list_filter = ('category',)
    search_fields = ('name',)
    autocomplete_fields = ('category',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = (ProductPhotoInline,)

    @display(description=_("Категории"))
    def display_categories(self, obj):
        return ", ".join([cat.name for cat in obj.category.all()])

    @display(description=_("Фото"))
    def display_photo(self, obj):
        if obj.photo:
            return mark_safe(
                f'<img src="{obj.photo.url}" height="120" width="120" '
                f'style="border-radius: 10%;" />')
