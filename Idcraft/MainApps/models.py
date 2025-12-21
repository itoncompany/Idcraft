from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static


class SchoolDetails(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='school_details')
    school_name = models.CharField(max_length=200)
    school_logo = models.ImageField(
        upload_to='school_logos/', blank=True, null=True)
    school_image = models.ImageField(
        upload_to='school_image/', blank=True, null=True)
    
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
    GRADE_CHOICES = [
        ('NURSERY', 'Nursery'),
        ('LKG', 'LKG'),
        ('UKG', 'UKG'),
        ('1', 'Grade I'),
        ('2', 'Grade II'),
        ('3', 'Grade III'),
        ('4', 'Grade IV'),
        ('5', 'Grade V'),
        ('6', 'Grade VI'),
        ('7', 'Grade VII'),
        ('8', 'Grade VIII'),
        ('9', 'Grade IX'),
        ('10', 'Grade X'),
        ('11', 'Grade XI'),
        ('12', 'Grade XII'),
        ('OTHER', 'Other'),  # Use lowercase key for consistency
    ]

    SECTION_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
        ('G', 'G'),
        ('H', 'H'),

    ] #this isf for
    ID_STATUS_CHOICES = [
    ('NEW', 'New'),
    ('ACTIVE', 'Active'),
    ('LOST', 'Lost'),
    ('REISSUED', 'Reissued'),
    ('EXPIRED', 'Expired'),
]


    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='student_profile'
    )
    full_name = models.CharField(max_length=150)
    roll = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, default='OTHER')
    email = models.EmailField(blank=True)
    student_phone = models.CharField(max_length=15, blank=True)
    parent_name = models.CharField(max_length=150, blank=True)
    parent_phone = models.CharField(max_length=15, blank=True)
    address=models.CharField(max_length=300, blank=True)
    photo = models.ImageField(
        upload_to='student_photos/', blank=True, null=True)
    school = models.ForeignKey(
        'SchoolDetails',
        on_delete=models.SET_NULL,
        null=True,
        related_name='students'
    )
    grade = models.CharField(
        max_length=10, choices=GRADE_CHOICES, default='OTHER')
    section = models.CharField(
        max_length=5, choices=SECTION_CHOICES, blank=True)
    valid_until = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=ID_STATUS_CHOICES, default='ACTIVE')

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        ordering = ['full_name']

    def __str__(self):
        return self.full_name

    def get_photo_url(self):
        """Return the student's photo URL or default if not uploaded."""
        if self.photo:
            return self.photo.url
        return static('default_student_photo.jpg')

    def get_id_card_url(self):
        """Return ID card image URL if exists."""
        if hasattr(self, 'id_card_image') and self.id_card_image:
            return self.id_card_image.url
        return None

    def get_school_name(self):
        """Return associated school name or 'N/A'."""
        return self.school.school_name if self.school else "N/A"

    def get_school_logo_url(self):
        """Return school logo URL or default."""
        if self.school and self.school.school_logo:
            return self.school.school_logo.url
        return static('default_school_logo.jpg')




class IDCardTemplate(models.Model):
    CARD_CHOICES = [('LOST','Lost'), ('RENEW','Renew'), ('NEW','New')]
    
    school = models.ForeignKey('SchoolDetails', on_delete=models.CASCADE, related_name='id_card_templates')
    template_image = models.ImageField(upload_to='id_card_templates/', blank=True, null=True, help_text="Background image of the ID card template")

    # ------------------ Photo ------------------
    photo_x = models.IntegerField(default=42)
    photo_y = models.IntegerField(default=127)
    photo_width = models.IntegerField(default=71)
    photo_height = models.IntegerField(default=71)
    photo_alignment = models.CharField(max_length=10, choices=[('left','Left'),('center','Center'),('right','Right')], default='center')
    photo_tag = models.CharField(max_length=50, default="Photo")
    photo_tag_active = models.BooleanField(default=True)
    photo_value_active = models.BooleanField(default=True)
    photo_tag_color = models.CharField(max_length=7, default="#000000")
    photo_value_color = models.CharField(max_length=7, default="#000000")

    # ------------------ Full Name ------------------
    full_name_x = models.IntegerField(default=20)
    full_name_y = models.IntegerField(default=100)
    full_name_font_size = models.IntegerField(default=12)
    full_name_font_family = models.CharField(max_length=50, default="Verdana")
    full_name_alignment = models.CharField(max_length=10, choices=[('left','Left'),('center','Center'),('right','Right')], default='left')
    full_name_tag = models.CharField(max_length=50, default="Full Name")
    full_name_tag_active = models.BooleanField(default=True)
    full_name_value_active = models.BooleanField(default=True)
    full_name_tag_color = models.CharField(max_length=7, default="#333333")
    full_name_value_color = models.CharField(max_length=7, default="#333333")

    # ------------------ Roll Number ------------------
    roll_x = models.IntegerField(default=20)
    roll_y = models.IntegerField(default=90)
    roll_font_size = models.IntegerField(default=8)
    roll_font_family = models.CharField(max_length=50, default="Verdana")
    roll_alignment = models.CharField(max_length=10, choices=[('left','Left'),('center','Center'),('right','Right')], default='left')
    roll_tag = models.CharField(max_length=50, default="Roll Number")
    roll_tag_active = models.BooleanField(default=True)
    roll_value_active = models.BooleanField(default=True)
    roll_tag_color = models.CharField(max_length=7, default="#333333")
    roll_value_color = models.CharField(max_length=7, default="#333333")

    # ------------------ Date of Birth ------------------
    dob_x = models.IntegerField(default=20)
    dob_y = models.IntegerField(default=80)
    dob_font_size = models.IntegerField(default=14)
    dob_font_family = models.CharField(max_length=50, default="Verdana")
    dob_alignment = models.CharField(max_length=10, choices=[('left','Left'),('center','Center'),('right','Right')], default='left')
    dob_tag = models.CharField(max_length=50, default="Date of Birth")
    dob_tag_active = models.BooleanField(default=True)
    dob_value_active = models.BooleanField(default=True)
    dob_tag_color = models.CharField(max_length=7, default="#333333")
    dob_value_color = models.CharField(max_length=7, default="#333333")

    # ------------------ Gender ------------------
    gender_x = models.IntegerField(default=20)
    gender_y = models.IntegerField(default=100)
    gender_font_size = models.IntegerField(default=8)
    gender_font_family = models.CharField(max_length=50, default="Verdana")
    gender_alignment = models.CharField(max_length=10, choices=[('left','Left'),('center','Center'),('right','Right')], default='left')
    gender_tag = models.CharField(max_length=50, default="Gender")
    gender_tag_active = models.BooleanField(default=True)
    gender_value_active = models.BooleanField(default=True)
    gender_tag_color = models.CharField(max_length=7, default="#333333")
    gender_value_color = models.CharField(max_length=7, default="#333333")

    # ------------------ Email ------------------
    email_x = models.IntegerField(default=20)
    email_y = models.IntegerField(default=120)
    email_font_size = models.IntegerField(default=12)
    email_font_family = models.CharField(max_length=50, default="Verdana")
    email_alignment = models.CharField(max_length=10, choices=[('left','Left'),('center','Center'),('right','Right')], default='left')
    email_tag = models.CharField(max_length=50, default="Email")
    email_tag_active = models.BooleanField(default=True)
    email_value_active = models.BooleanField(default=True)
    email_tag_color = models.CharField(max_length=7, default="#333333")
    email_value_color = models.CharField(max_length=7, default="#333333")

    # ------------------ Student Phone ------------------
    student_phone_x = models.IntegerField(default=20)
    student_phone_y = models.IntegerField(default=140)
    student_phone_font_size = models.IntegerField(default=12)
    student_phone_font_family = models.CharField(max_length=50, default="Verdana")
    student_phone_alignment = models.CharField(max_length=10, choices=[('left','Left'),('center','Center'),('right','Right')], default='left')
    student_phone_tag = models.CharField(max_length=50, default="Student Phone")
    student_phone_tag_active = models.BooleanField(default=True)
    student_phone_value_active = models.BooleanField(default=True)
    student_phone_tag_color = models.CharField(max_length=7, default="#333333")
    student_phone_value_color = models.CharField(max_length=7, default="#333333")

    # ------------------ Parent Name ------------------
    parent_name_x = models.IntegerField(default=20)
    parent_name_y = models.IntegerField(default=50)
    parent_name_font_size = models.IntegerField(default=8)
    parent_name_font_family = models.CharField(max_length=50, default="Verdana")
    parent_name_alignment = models.CharField(max_length=10, choices=[('left','Left'),('center','Center'),('right','Right')], default='left')
    parent_name_tag = models.CharField(max_length=50, default="Parent Name")
    parent_name_tag_active = models.BooleanField(default=True)
    parent_name_value_active = models.BooleanField(default=True)
    parent_name_tag_color = models.CharField(max_length=7, default="#333333")
    parent_name_value_color = models.CharField(max_length=7, default="#333333")

    # ------------------ Parent Phone ------------------
    parent_phone_x = models.IntegerField(default=20)
    parent_phone_y = models.IntegerField(default=60)
    parent_phone_font_size = models.IntegerField(default=8)
    parent_phone_font_family = models.CharField(max_length=50, default="Verdana")
    parent_phone_alignment = models.CharField(max_length=10, choices=[('left','Left'),('center','Center'),('right','Right')], default='left')
    parent_phone_tag = models.CharField(max_length=50, default="Parent Phone")
    parent_phone_tag_active = models.BooleanField(default=True)
    parent_phone_value_active = models.BooleanField(default=True)
    parent_phone_tag_color = models.CharField(max_length=7, default="#333333")
    parent_phone_value_color = models.CharField(max_length=7, default="#333333")

    # ------------------ Address ------------------
    address_x = models.IntegerField(default=20)
    address_y = models.IntegerField(default=40)
    address_font_size = models.IntegerField(default=8)
    address_font_family = models.CharField(max_length=50, default="Verdana")
    address_alignment = models.CharField(max_length=10, choices=[('left','Left'),('center','Center'),('right','Right')], default='left')
    address_tag = models.CharField(max_length=50, default="Address")
    address_tag_active = models.BooleanField(default=True)
    address_value_active = models.BooleanField(default=True)
    address_tag_color = models.CharField(max_length=7, default="#333333")
    address_value_color = models.CharField(max_length=7, default="#333333")

    # ------------------ School Name ------------------
    school_name_x = models.IntegerField(default=20)
    school_name_y = models.IntegerField(default=220)
    school_name_font_size = models.IntegerField(default=10)
    school_name_font_family = models.CharField(max_length=50, default="Verdana")
    school_name_alignment = models.CharField(max_length=10, choices=[('left','Left'),('center','Center'),('right','Right')], default='left')
    school_name_tag = models.CharField(max_length=50, default="School Name")
    school_name_tag_active = models.BooleanField(default=True)
    school_name_value_active = models.BooleanField(default=True)
    school_name_tag_color = models.CharField(max_length=7, default="#333333")
    school_name_value_color = models.CharField(max_length=7, default="#333333")

    # ------------------ Grade/Class ------------------
    grade_x = models.IntegerField(default=20)
    grade_y = models.IntegerField(default=70)
    grade_font_size = models.IntegerField(default=8)
    grade_font_family = models.CharField(max_length=50, default="Verdana")
    grade_alignment = models.CharField(max_length=10, choices=[('left','Left'),('center','Center'),('right','Right')], default='left')
    grade_tag = models.CharField(max_length=50, default="Grade/Class")
    grade_tag_active = models.BooleanField(default=True)
    grade_value_active = models.BooleanField(default=True)
    grade_tag_color = models.CharField(max_length=7, default="#333333")
    grade_value_color = models.CharField(max_length=7, default="#333333")

    # ------------------ Section ------------------
    section_x = models.IntegerField(default=20)
    section_y = models.IntegerField(default=69)
    section_font_size = models.IntegerField(default=8)
    section_font_family = models.CharField(max_length=50, default="Verdana")
    section_alignment = models.CharField(max_length=10, choices=[('left','Left'),('center','Center'),('right','Right')], default='left')
    section_tag = models.CharField(max_length=50, default="Section")
    section_tag_active = models.BooleanField(default=True)
    section_value_active = models.BooleanField(default=True)
    section_tag_color = models.CharField(max_length=7, default="#333333")
    section_value_color = models.CharField(max_length=7, default="#333333")

    # ------------------ Valid Until ------------------
    valid_until_x = models.IntegerField(default=20)
    valid_until_y = models.IntegerField(default=30)
    valid_until_font_size = models.IntegerField(default=8)
    valid_until_font_family = models.CharField(max_length=50, default="Verdana")
    valid_until_alignment = models.CharField(max_length=10, choices=[('left','Left'),('center','Center'),('right','Right')], default='left')
    valid_until_tag = models.CharField(max_length=50, default="Valid Until")
    valid_until_tag_active = models.BooleanField(default=True)
    valid_until_value_active = models.BooleanField(default=True)
    valid_until_tag_color = models.CharField(max_length=7, default="#333333")
    valid_until_value_color = models.CharField(max_length=7, default="#333333")

    def __str__(self):
        return self.school.school_name 