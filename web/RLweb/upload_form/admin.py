# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from upload_form.models import FileNameModel


class FileNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_name', 'upload_time')
    list_display_links = ('id', 'file_name')

admin.site.register(FileNameModel, FileNameAdmin)
