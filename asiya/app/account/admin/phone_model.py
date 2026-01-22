from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from ..models import PhoneModel


@admin.register(PhoneModel)
class PhoneModelAdmin(UnfoldModelAdmin):
    list_display = ('brand', 'model_name')
