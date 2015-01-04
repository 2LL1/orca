from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from django.contrib import admin
from orca.models import Ocean, Alpha, Universe, Category


class OceanAdmin(admin.ModelAdmin):
    pass
admin.site.register(Ocean, OceanAdmin)

class AlphaAdmin(admin.ModelAdmin):
    pass
admin.site.register(Alpha, AlphaAdmin)

class UniverseAdmin(admin.ModelAdmin):
    pass
admin.site.register(Universe, UniverseAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)

