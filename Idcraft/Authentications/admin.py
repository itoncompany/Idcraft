from django.contrib import admin
from django.utils.html import format_html
from Authentications.models import Profile,CompanyDetails,CompanyPaymentDetails,PaymentDetails,ServicePrice,TeamMember


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'profile_picture', 'ph_num', 'city', 'created_at')
    search_fields = ('user__username', 'full_name', 'ph_num', 'city')
    list_filter = ('gender', 'city', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

    def profile_picture(self, obj):
        if obj.pr_pic:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />', obj.pr_pic.url)
        return "No Image"
    profile_picture.short_description = "Profile Picture"




@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'company', 'is_active', 'created_at')
    list_filter = ('is_active', 'company', 'role')
    search_fields = ('name', 'role', 'company__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)



@admin.register(CompanyDetails)
class CompanyDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'app_name', 
        'company_name',
        'whatsapp_number', 
        'email', 
        'phone', 
        'website', 
        'is_active', 
        'created_at', 
        'updated_at'
    )
    search_fields = ('app_name', 'company_name', 'email', 'phone', 'website')
    list_filter = ('is_active', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('app_name', 'company_name', 'tagline', 'description', 'logo', 'address', 'email', 'phone')
        }),
        ('App Files', {
            'fields': ('android_app_file', 'android_version', 'ios_app_file', 'ios_version', 'desktop_app_file', 'desktop_version')
        }),
        ('Social Links', {
            'fields': ('whatsapp_number','facebook_link', 'twitter_link', 'linkedin_link', 'instagram_link', 'website')
        }),
        ('Status & Tracking', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" />', obj.logo.url)
        return "-"
    logo_preview.short_description = 'Logo'






@admin.register(CompanyPaymentDetails)
class CompanyPaymentDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'company',
        'payment_method',
        'active_status',
        'qrcode_preview',
        'created_at'
    )
    search_fields = ('company__company_name',)
    list_filter = ('payment_method', 'is_active', 'created_at')
    ordering = ('-created_at',)

    def qrcode_preview(self, obj):
        if obj.qrcode:
            return format_html('<img src="{}" width="80" />', obj.qrcode.url)
        return "-"
    qrcode_preview.short_description = "QR Code"

    def active_status(self, obj):
        return "Active" if obj.is_active else "Inactive"
    active_status.short_description = "Status"

# -----------------------------
# Payment Details Admin
# -----------------------------
@admin.register(PaymentDetails)
class PaymentDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'transaction_id',
        'user',
        'payment_method',
        'amount',
        'status',
        'payment_preview',
        'created_at'
    )
    search_fields = ('transaction_id', 'user__username')
    list_filter = ('payment_method', 'status', 'created_at')
    ordering = ('-created_at',)

    def payment_preview(self, obj):
        if obj.payment_image:
            return format_html('<img src="{}" width="80" />', obj.payment_image.url)
        return "-"
    payment_preview.short_description = "Payment Screenshot"




@admin.register(ServicePrice)
class ServicePriceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'company', 'price', 'is_active', 'created_at')
    search_fields = ('service_name', 'company__company_name')
    list_filter = ('is_active', 'company')
    ordering = ('service_name',)