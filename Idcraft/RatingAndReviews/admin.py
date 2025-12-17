from django.contrib import admin
from RatingAndReviews.models import Feedback
# Register your models here.

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'user', 
        'name', 
        'rating', 
        'is_public', 
        'created_at'
    )
    list_filter = ('rating', 'is_public', 'created_at')
    search_fields = ('name',  'comments', 'user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at', 'ip_address')

    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'profile_image', 'rating', 'comments', 'is_public', 'ip_address')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def profile_image_tag(self, obj):
        if obj.profile_image:
            return f'<img src="{obj.profile_image.url}" width="50" height="50" style="object-fit: cover; border-radius:50%;" />'
        return '-'
    profile_image_tag.allow_tags = True
    profile_image_tag.short_description = 'Profile Image'