"""
apps/careers/models.py
"""

from django.db import models
from urllib.parse import quote


class CareerDepartment(models.Model):
    name          = models.CharField(max_length=200, help_text='e.g. Sales Department')
    icon          = models.CharField(max_length=100, blank=True, help_text='Emoji or icon class e.g. 🛵')
    display_order = models.PositiveIntegerField(default=0)
    is_active     = models.BooleanField(default=True)

    class Meta:
        ordering            = ['display_order', 'name']
        verbose_name        = 'Career Department'
        verbose_name_plural = 'Career Departments'

    def __str__(self):
        return self.name


class CareerRole(models.Model):
    department      = models.ForeignKey(
        CareerDepartment,
        on_delete=models.CASCADE,
        related_name='roles',
    )
    title           = models.CharField(max_length=200, help_text='e.g. Field Staff')
    whatsapp_number = models.CharField(
        max_length=20,
        help_text='WhatsApp number with country code — digits only, no + or spaces. e.g. 919876543210',
    )
    whatsapp_message = models.CharField(
        max_length=500,
        blank=True,
        help_text='Pre-filled message. Leave blank to auto-generate from job title.',
    )
    display_order = models.PositiveIntegerField(default=0)
    is_active     = models.BooleanField(default=True)

    class Meta:
        ordering            = ['display_order', 'title']
        verbose_name        = 'Career Role'
        verbose_name_plural = 'Career Roles'

    def __str__(self):
        return f"{self.department.name} — {self.title}"

    def _clean_number(self):
        """
        Strips +, spaces, dashes, brackets from the stored number.
        Ensures wa.me gets pure digits only: 919876543210
        """
        import re
        return re.sub(r'[^\d]', '', self.whatsapp_number)

    def get_whatsapp_url(self):
        """
        Builds a correct wa.me link:
          https://wa.me/919876543210?text=Hi%2C+I+am+interested+in+Field+Staff

        Common mistakes fixed:
          • Strips + prefix (causes double-encoding → api.whatsapp.com 404)
          • Strips spaces / dashes from number
          • Uses quote(safe='') for clean single-encoding of message
        """
        number  = self._clean_number()
        message = (
            self.whatsapp_message.strip()
            or f"Hi, I am interested in the {self.title} position at TagsBikez."
        )
        return f"https://wa.me/{number}?text={quote(message, safe='')}"