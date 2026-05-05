from django.db import models
from accounts.models import CustomUser


class Subscription(models.Model):
    subscriber_name = models.CharField(max_length=255)
    subscription_plan = models.CharField(max_length=255)
    subscription_cost = models.FloatField()
    paypal_subscription_id = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    subscription2customuser = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                                   related_name='customuser2subscription')

    def __str__(self):
        return f"{self.subscriber_name} - {self.subscription_plan} subscription"
