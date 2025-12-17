from django.contrib import admin
from MainApps.models import SchoolDetails, Student,IDCardTemplate

@admin.register(SchoolDetails)
class SchoolDetailsAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'contact_email', 'contact_phone', 'website', 'created_at')
    search_fields = ('school_name', 'contact_email', 'contact_phone')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')



@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'get_school_name', 'email', 'student_phone', 'gender', 'created_at')
    search_fields = ('full_name', 'email', 'student_phone', 'school__school_name')
    list_filter = ('gender', 'school', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

    def get_school_name(self, obj):
        return obj.school.school_name if obj.school else 'N/A'
    get_school_name.short_description = 'School'





@admin.register(IDCardTemplate)
class IDCardTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'template_image')
    list_filter = ('school',)
    search_fields = ('name',)

    fieldsets = (
        ('General', {
            'fields': ('school', 'name', 'template_image')
        }),
        ('Photo Settings', {
            'fields': ('photo_x', 'photo_y', 'photo_width', 'photo_height', 'photo_alignment')
        }),
        ('Full Name', {
            'fields': ('full_name_x', 'full_name_y', 'full_name_font_size', 'full_name_font_color', 'full_name_font_family', 'full_name_alignment')
        }),
        ('Roll Number', {
            'fields': ('roll_x', 'roll_y', 'roll_font_size', 'roll_font_color', 'roll_font_family', 'roll_alignment')
        }),
        ('Date of Birth', {
            'fields': ('dob_x', 'dob_y', 'dob_font_size', 'dob_font_color', 'dob_font_family', 'dob_alignment')
        }),
        ('Gender', {
            'fields': ('gender_x', 'gender_y', 'gender_font_size', 'gender_font_color', 'gender_font_family', 'gender_alignment')
        }),
        ('Email', {
            'fields': ('email_x', 'email_y', 'email_font_size', 'email_font_color', 'email_font_family', 'email_alignment')
        }),
        ('Student Phone', {
            'fields': ('student_phone_x', 'student_phone_y', 'student_phone_font_size', 'student_phone_font_color', 'student_phone_font_family', 'student_phone_alignment')
        }),
        ('Parent Name', {
            'fields': ('parent_name_x', 'parent_name_y', 'parent_name_font_size', 'parent_name_font_color', 'parent_name_font_family', 'parent_name_alignment')
        }),
        ('Parent Phone', {
            'fields': ('parent_phone_x', 'parent_phone_y', 'parent_phone_font_size', 'parent_phone_font_color', 'parent_phone_font_family', 'parent_phone_alignment')
        }),
        ('Address', {
            'fields': ('address_x', 'address_y', 'address_font_size', 'address_font_color', 'address_font_family', 'address_alignment')
        }),
        ('School', {
            'fields': ('school_x', 'school_y', 'school_font_size', 'school_font_color', 'school_font_family', 'school_alignment')
        }),
        ('Grade/Class', {
            'fields': ('grade_x', 'grade_y', 'grade_font_size', 'grade_font_color', 'grade_font_family', 'grade_alignment')
        }),
        ('Section', {
            'fields': ('section_x', 'section_y', 'section_font_size', 'section_font_color', 'section_font_family', 'section_alignment')
        }),
        ('Valid Until', {
            'fields': ('valid_until_x', 'valid_until_y', 'valid_until_font_size', 'valid_until_font_color', 'valid_until_font_family', 'valid_until_alignment')
        }),
    )