import uuid

from django.utils import timezone
from django.db import models


class OTPmodel(models.Model):
    otp_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    otp = models.CharField(max_length=100)
    student_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    expired_at = models.DateTimeField()
    is_successful = models.BooleanField(default=False)
