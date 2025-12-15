from django.contrib import admin
from MainApps.models import SchoolDetails, Student

@admin.register(SchoolDetails)
class SchoolDetailsAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'contact_email', 'contact_phone', 'website', 'created_at')
    search_fields = ('school_name', 'contact_email', 'contact_phone')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'get_school_name', 'email', 'phone', 'gender', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'school__school_name')
    list_filter = ('gender', 'school', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

    def get_school_name(self, obj):
        return obj.school.school_name if obj.school else 'N/A'
    get_school_name.short_description = 'School'
