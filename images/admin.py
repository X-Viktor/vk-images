from django.contrib import admin

from images.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'hash']
    readonly_fields = ['id', 'hash', 'image', 'proportions', 'created_at']
    search_fields = ['hash']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
