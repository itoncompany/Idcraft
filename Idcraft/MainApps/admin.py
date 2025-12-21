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
    list_display = ( 'school', 'template_image')
    list_filter = ('school',)
    search_fields = ('school__school_name',)

    fieldsets = (
        ('General', {
            'fields': ('school', 'template_image')
        }),

        # ------------------ Photo ------------------
        ('Photo Settings', {
            'fields': (
                'photo_x', 'photo_y', 'photo_width', 'photo_height', 'photo_alignment',
                'photo_tag', 'photo_tag_active', 'photo_value_active',
                'photo_tag_color', 'photo_value_color'
            )
        }),

        # ------------------ Full Name ------------------
        ('Full Name', {
            'fields': (
                'full_name_x', 'full_name_y', 'full_name_font_size', 'full_name_font_family', 'full_name_alignment',
                'full_name_tag', 'full_name_tag_active', 'full_name_value_active',
                'full_name_tag_color', 'full_name_value_color'
            )
        }),

        # ------------------ Roll Number ------------------
        ('Roll Number', {
            'fields': (
                'roll_x', 'roll_y', 'roll_font_size', 'roll_font_family', 'roll_alignment',
                'roll_tag', 'roll_tag_active', 'roll_value_active',
                'roll_tag_color', 'roll_value_color'
            )
        }),

        # ------------------ Date of Birth ------------------
        ('Date of Birth', {
            'fields': (
                'dob_x', 'dob_y', 'dob_font_size', 'dob_font_family', 'dob_alignment',
                'dob_tag', 'dob_tag_active', 'dob_value_active',
                'dob_tag_color', 'dob_value_color'
            )
        }),

        # ------------------ Gender ------------------
        ('Gender', {
            'fields': (
                'gender_x', 'gender_y', 'gender_font_size', 'gender_font_family', 'gender_alignment',
                'gender_tag', 'gender_tag_active', 'gender_value_active',
                'gender_tag_color', 'gender_value_color'
            )
        }),

        # ------------------ Email ------------------
        ('Email', {
            'fields': (
                'email_x', 'email_y', 'email_font_size', 'email_font_family', 'email_alignment',
                'email_tag', 'email_tag_active', 'email_value_active',
                'email_tag_color', 'email_value_color'
            )
        }),

        # ------------------ Student Phone ------------------
        ('Student Phone', {
            'fields': (
                'student_phone_x', 'student_phone_y', 'student_phone_font_size', 'student_phone_font_family', 'student_phone_alignment',
                'student_phone_tag', 'student_phone_tag_active', 'student_phone_value_active',
                'student_phone_tag_color', 'student_phone_value_color'
            )
        }),

        # ------------------ Parent Name ------------------
        ('Parent Name', {
            'fields': (
                'parent_name_x', 'parent_name_y', 'parent_name_font_size', 'parent_name_font_family', 'parent_name_alignment',
                'parent_name_tag', 'parent_name_tag_active', 'parent_name_value_active',
                'parent_name_tag_color', 'parent_name_value_color'
            )
        }),

        # ------------------ Parent Phone ------------------
        ('Parent Phone', {
            'fields': (
                'parent_phone_x', 'parent_phone_y', 'parent_phone_font_size', 'parent_phone_font_family', 'parent_phone_alignment',
                'parent_phone_tag', 'parent_phone_tag_active', 'parent_phone_value_active',
                'parent_phone_tag_color', 'parent_phone_value_color'
            )
        }),

        # ------------------ Address ------------------
        ('Address', {
            'fields': (
                'address_x', 'address_y', 'address_font_size', 'address_font_family', 'address_alignment',
                'address_tag', 'address_tag_active', 'address_value_active',
                'address_tag_color', 'address_value_color'
            )
        }),

        # ------------------ School Name ------------------
        ('School Name', {
            'fields': (
                'school_name_x', 'school_name_y', 'school_name_font_size', 'school_name_font_family', 'school_name_alignment',
                'school_name_tag', 'school_name_tag_active', 'school_name_value_active',
                'school_name_tag_color', 'school_name_value_color'
            )
        }),

        # ------------------ Grade/Class ------------------
        ('Grade/Class', {
            'fields': (
                'grade_x', 'grade_y', 'grade_font_size', 'grade_font_family', 'grade_alignment',
                'grade_tag', 'grade_tag_active', 'grade_value_active',
                'grade_tag_color', 'grade_value_color'
            )
        }),

        # ------------------ Section ------------------
        ('Section', {
            'fields': (
                'section_x', 'section_y', 'section_font_size', 'section_font_family', 'section_alignment',
                'section_tag', 'section_tag_active', 'section_value_active',
                'section_tag_color', 'section_value_color'
            )
        }),

        # ------------------ Valid Until ------------------
        ('Valid Until', {
            'fields': (
                'valid_until_x', 'valid_until_y', 'valid_until_font_size', 'valid_until_font_family', 'valid_until_alignment',
                'valid_until_tag', 'valid_until_tag_active', 'valid_until_value_active',
                'valid_until_tag_color', 'valid_until_value_color'
            )
        }),
    )