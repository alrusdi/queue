from django.contrib import admin
from queue.models import Company, MenuItem, MenuItemAttribute

admin.site.register(Company)

class MenuItemAttributeInline(admin.TabularInline):
    model = MenuItemAttribute
    max_num = 3
    extra = 0

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'company')
    list_filter = ['company']
    search_fields = ['title']
    inlines = [MenuItemAttributeInline]
admin.site.register(MenuItem, MenuItemAdmin)



