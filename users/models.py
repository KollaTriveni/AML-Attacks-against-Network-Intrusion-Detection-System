from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    STATUS_CHOICES = (
        ('PENDING', 'PENDING'),
        ('APPROVED', 'APPROVED'),
        ('DENIED', 'DENIED'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    mobile = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

class UserOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

from django.db import models

class NetworkInput(models.Model):
    flow_duration = models.FloatField()
    total_fwd_packets = models.FloatField()
    total_bwd_packets = models.FloatField()
    fwd_pkt_len_mean = models.FloatField()
    bwd_pkt_len_mean = models.FloatField()
    pkt_len_variance = models.FloatField()

    predicted_attack = models.CharField(max_length=100, blank=True, null=True)
    confidence = models.FloatField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction at {self.created_at}"



