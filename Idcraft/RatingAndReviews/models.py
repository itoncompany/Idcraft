from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Feedback(models.Model):
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='feedbacks'
    )
    name = models.CharField(max_length=120, blank=True)

    # ⭐ Store user photo for public feedback
    profile_image = models.ImageField(
        upload_to='feedback_profile/',
        blank=True,
        null=True
    )

    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comments = models.TextField()
    is_public = models.BooleanField(default=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'

    def __str__(self):
        who = self.name or (self.user.get_full_name() if self.user else 'Anonymous')
        return f'{who} — {self.rating} ★ — {self.created_at:%Y-%m-%d %H:%M}'
