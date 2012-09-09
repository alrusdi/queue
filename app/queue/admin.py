from django.contrib import admin
from queue.models import Company, MenuItem

admin.site.register(Company)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'company')
    list_filter = ['company']
    search_fields = ['title']
admin.site.register(MenuItem, MenuItemAdmin)
