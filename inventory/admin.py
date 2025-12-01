from django.contrib import admin
from .models import Tag, Category, Inventory, Unit

admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Inventory)
admin.site.register(Unit)