from django.contrib import admin

from petstagram.common.models import Comment, Like

admin.site.register(Comment)
admin.site.register(Like)
