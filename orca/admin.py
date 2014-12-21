from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from django.contrib import admin
from orca.models import Alpha, Universe, Category


class AlphaAdmin(admin.ModelAdmin):
    pass
admin.site.register(Alpha, AlphaAdmin)

class UniverseAdmin(admin.ModelAdmin):
    pass
admin.site.register(Universe, UniverseAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)

