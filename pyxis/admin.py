from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from django.contrib import admin

from pyxis.models import Account, Command


class AccountAdmin(admin.ModelAdmin):
    pass
admin.site.register(Account, AccountAdmin)

class CommandAdmin(admin.ModelAdmin):
    pass
admin.site.register(Command, CommandAdmin)

