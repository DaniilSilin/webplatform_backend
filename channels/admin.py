from django.contrib import admin

from .models import Channel


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "owner")
    search_fields = ("title", "slug", "owner__email")
