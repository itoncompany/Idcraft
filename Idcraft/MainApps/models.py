from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static


class SchoolDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='school_details')
    school_name = models.CharField(max_length=200)
    school_logo = models.ImageField(upload_to='school_logos/', blank=True, null=True)
    school_student_id_card_template = models.ImageField(upload_to='student_id_cards/', blank=True, null=True)
    address = models.CharField(max_length=300)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15, blank=True)
    website = models.URLField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'School Detail'
        verbose_name_plural = 'School Details'
        ordering = ['-created_at']

    def __str__(self):
        return self.school_name

    def get_logo_url(self):
        if self.school_logo:
            return self.school_logo.url
        return static('default_school_logo.jpg')


class Student(models.Model):
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='student_profile')
    full_name = models.CharField(max_length=150)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='OTHER')
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    school = models.ForeignKey(SchoolDetails, on_delete=models.SET_NULL, null=True, related_name='students')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        ordering = ['full_name']

    def __str__(self):
        return self.full_name

    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        return static('default_student_photo.jpg')

    def get_id_card_url(self):
        if hasattr(self, 'id_card_image') and self.id_card_image:
            return self.id_card_image.url
        return None

    def get_school_name(self):
        if self.school:
            return self.school.school_name
        return "N/A"

    def get_school_logo_url(self):
        if self.school and self.school.school_logo:
            return self.school.school_logo.url
        return static('default_school_logo.jpg')