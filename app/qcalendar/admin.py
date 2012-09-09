from django.contrib import admin
from qcalendar.models import Calendar, Day

class DayInline(admin.TabularInline):
    model = Day
    max_num = 366
    extra = 365

class CalendarAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'company')
    list_filter = ['company', 'year']
    search_fields = ['title']
    inlines = [DayInline]
    save_as = True
admin.site.register(Calendar, CalendarAdmin)



