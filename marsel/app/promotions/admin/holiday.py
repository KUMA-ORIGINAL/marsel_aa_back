from django.contrib import admin

from unfold.admin import ModelAdmin as UnfoldModelAdmin

from promotions.models import Holiday


@admin.register(Holiday)
class HolidayAdmin(UnfoldModelAdmin):
    list_display = ('name', 'month', 'day')
    autocomplete_fields = ('products',)