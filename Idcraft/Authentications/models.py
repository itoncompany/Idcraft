from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.core.files.base import ContentFile
from django.dispatch import receiver
from django.contrib import messages
from django.shortcuts import redirect
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added, social_account_updated
from django.contrib.auth.signals import user_logged_in
import requests
import os

# Create your models here.


class CompanyDetails(models.Model):
    app_name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='company_logos/')
    tagline = models.CharField(max_length=255, blank=True)  # optional short description
    description = models.TextField(blank=True)  # detailed company description
    address = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    
    # App files for download
    android_app_file = models.FileField(upload_to='apps/android/', blank=True, null=True)
    ios_app_file = models.FileField(upload_to='apps/ios/', blank=True, null=True)
    desktop_app_file = models.FileField(upload_to='apps/desktop/', blank=True, null=True)
    
    # App version info (optional)
    android_version = models.CharField(max_length=20, blank=True)
    ios_version = models.CharField(max_length=20, blank=True)
    desktop_version = models.CharField(max_length=20, blank=True)
    
    # Social links
    facebook_link = models.URLField(blank=True)
    twitter_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)
    whatsapp_number = models.CharField(max_length=15, blank=True)
    website = models.URLField(blank=True)
    
    # Status / Tracking
    is_active = models.BooleanField(default=True)  # To mark company as active/inactive
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.company_name




class CompanyPaymentDetails(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('esewa', 'eSewa'),
        ('khalti', 'Khalti'),
        ('bank', 'Bank Transfer'),
        ('cash', 'Cash'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    company = models.ForeignKey(CompanyDetails, on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    qrcode = models.ImageField(upload_to='payment_screenshots/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company} - {self.payment_method}"






class PaymentDetails(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('esewa', 'eSewa'),
        ('khalti', 'Khalti'),
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_image = models.ImageField(upload_to='payment_screenshots/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.user}"




class TeamMember(models.Model):
    company = models.ForeignKey(CompanyDetails, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='team_photos/', blank=True, null=True)
    bio = models.TextField(blank=True)
    linkedin_link = models.URLField(blank=True)
    twitter_link = models.URLField(blank=True)
    facebook_link = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.role}"




class ServicePrice(models.Model):
    PAYMENT_FREQUENCY_CHOICES = (
        ('monthly', 'Monthly'),
        ('annually', 'Annually'),
    )

    company = models.ForeignKey(
        CompanyDetails, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="Optional: Link service price to a specific company"
    )
    service_name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    price = models.CharField(max_length=10)
    frequency = models.CharField(
        max_length=10,
        choices=PAYMENT_FREQUENCY_CHOICES,
        default='monthly'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['service_name']
        verbose_name = "Service Price"
        verbose_name_plural = "Service Prices"

    def __str__(self):
        return f"{self.service_name} - {self.price} ({self.frequency})"

class Profile(models.Model):
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150, blank=True)
    ph_num = models.CharField(max_length=10, blank=True)
    pr_pic = models.ImageField(upload_to='profile_pic/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='OTHER')
    website = models.URLField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.ph_num or 'N/A'}"

    def get_contact_info(self):
        return f"Email: {self.user.email}, Phone: {self.ph_num or 'N/A'}"

    def get_full_name(self):
        return self.full_name or self.user.get_full_name() or self.user.username

    def get_profile_picture_url(self):
        if self.pr_pic:
            return self.pr_pic.url
        return static('default_profile_pic.jpg')

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ['-created_at']





def create_or_update_profile(user, socialaccount=None, request=None):
    profile, created = Profile.objects.get_or_create(user=user)
    updated = False

    if socialaccount:
        extra_data = socialaccount.extra_data

        full_name = extra_data.get("name") or extra_data.get("full_name")
        if full_name and full_name != profile.full_name:
            profile.full_name = full_name
            updated = True

        profile_pic_url = extra_data.get("picture") or extra_data.get("profile_picture") or extra_data.get("avatar_url")
        if profile_pic_url and not profile.pr_pic:
            try:
                response = requests.get(profile_pic_url)
                if response.status_code == 200:
                    file_name = os.path.basename(profile_pic_url.split("?")[0])
                    profile.pr_pic.save(file_name, ContentFile(response.content), save=False)
                    updated = True
            except Exception as e:
                print(f"Failed to download profile picture: {e}")

        if extra_data.get("email") and not user.email:
            user.email = extra_data.get("email")
            user.save()
            updated = True

    profile.save()

    if request:
        if created:
            messages.success(request, "Profile created successfully!")
        elif updated:
            messages.success(request, "Profile updated successfully!")

# -----------------------------
# Signals
# -----------------------------
@receiver(user_signed_up)
def handle_user_signed_up(sender, request, user, **kwargs):
    # user.is_active = False
    # user.save()

    socialaccount = user.socialaccount_set.first()
    create_or_update_profile(user, socialaccount, request=request)

@receiver(social_account_added)
def handle_social_account_added(sender, request, sociallogin, **kwargs):
    create_or_update_profile(sociallogin.user, sociallogin.account, request=request)

@receiver(social_account_updated)
def handle_social_account_updated(sender, request, sociallogin, **kwargs):
    create_or_update_profile(sociallogin.user, sociallogin.account, request=request)

@receiver(user_logged_in)
def show_login_message(sender, request, user, **kwargs):
    messages.success(request, f"Welcome back, {user.username}!")