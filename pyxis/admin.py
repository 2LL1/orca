from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from django.contrib import admin

from pyxis.models import Account, Command


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'password')
admin.site.register(Account, AccountAdmin)

class CommandAdmin(admin.ModelAdmin):
    list_display = ('account', 'name', 'command', 'work_folder')
    list_display_links = ('name',)
admin.site.register(Command, CommandAdmin)

