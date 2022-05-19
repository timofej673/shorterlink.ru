from django.contrib import admin
from main.models import ShortLink

class ShortLinkAdmin(admin.ModelAdmin):
    pass


admin.site.register(ShortLink, ShortLinkAdmin)