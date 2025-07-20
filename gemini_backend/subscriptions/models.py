from django.db import models
from django.utils import timezone
from django.conf import settings

class Subscription(models.Model):
    PLAN_CHOICES = (
        ('basic', 'Basic'),
        ('pro', 'Pro'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='basic')
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan}"
