from django.db import models
import random
import string
from django.utils import timezone


class SMSCode(models.Model):
    phone = models.CharField(max_length=20)
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        # 5 daqiqa ichida amal qiladi
        return not self.is_used and (timezone.now() - self.created_at).seconds < 300

    @classmethod
    def generate_code(cls):
        return ''.join(random.choices(string.digits, k=4))

    class Meta:
        verbose_name = 'SMS Kod'
        verbose_name_plural = 'SMS Kodlar'
        ordering = ['-created_at']
