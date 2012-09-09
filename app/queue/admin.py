from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from queue.models import Company, MenuItem, MenuItemAttribute

class CompanyAdmin(MPTTModelAdmin):
    pass
admin.site.register(Company, CompanyAdmin)

class MenuItemAttributeInline(admin.TabularInline):
    model = MenuItemAttribute
    max_num = 3
    extra = 0

class MenuItemAdmin(MPTTModelAdmin):
    list_display = ('title', 'parent', 'company')
    list_filter = ['company']
    search_fields = ['title']
    inlines = [MenuItemAttributeInline]
admin.site.register(MenuItem, MenuItemAdmin)



