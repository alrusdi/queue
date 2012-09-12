from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from queue.models import *

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

class VisitAttributesInline(admin.TabularInline):
    model = VisitAttributes
    max_num = 3
    extra = 0

class OperatorAdmin(admin.ModelAdmin):
    list_filter = ['company']
admin.site.register(Operator, OperatorAdmin)

class VisitorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Visitor, VisitorAdmin)

class VisitRequestAdmin(admin.ModelAdmin):
    inlines = [VisitAttributesInline]
admin.site.register(VisitRequest, VisitRequestAdmin)

class VisitingPointAdmin(admin.ModelAdmin):
    pass
admin.site.register(VisitingPoint, VisitingPointAdmin)
