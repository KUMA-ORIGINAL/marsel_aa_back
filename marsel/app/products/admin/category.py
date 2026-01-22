from django.contrib import admin

from unfold.admin import ModelAdmin as UnfoldModelAdmin

from ..models import Category


@admin.register(Category)
class CategoryAdmin(UnfoldModelAdmin):
    list_display = ('id', 'name', 'parent',)
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('parent',)

    fieldsets = (
        (None, {'fields': ('name', 'parent', 'published')}),
    )
