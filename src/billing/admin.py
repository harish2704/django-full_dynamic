from django.contrib import admin
from eav.admin import BaseEntityAdmin, BaseSchemaAdmin
from billing.models import *
from billing.forms import *


class ItemAdmin(BaseEntityAdmin):
    form = ItemForm


class SchemaInline(admin.TabularInline):
    model = Schema


class EntityAdmin(admin.ModelAdmin):
    inlines = [
        # SchemaInline,
    ]


admin.site.register(Item, ItemAdmin)
admin.site.register(Entity,EntityAdmin)
admin.site.register(Schema, BaseSchemaAdmin)
admin.site.register(Choice)
admin.site.register(Thread)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderedItem)











# vim: set ft=python.django:
