"""
apps/careers/models.py

Models:
  CareerDepartment  — e.g. "Sales Department", "Service Department"
  CareerRole        — e.g. "Field Staff", "Technician"
                      Apply button links to WhatsApp with pre-filled message.

Page layout:
  [CareerDepartment]         ← SALES DEPARTMENT
    [CareerRole × N]         ← Field Staff    [APPLY NOW → WhatsApp]
    [CareerRole × N]         ← Sales Consultant [APPLY NOW → WhatsApp]
  [CareerDepartment]         ← SERVICE DEPARTMENT
    [CareerRole × N]         ← Technician     [APPLY NOW → WhatsApp]
"""

from django.db import models


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
    department    = models.ForeignKey(
        CareerDepartment,
        on_delete=models.CASCADE,
        related_name='roles',
    )
    title         = models.CharField(max_length=200, help_text='e.g. Field Staff')
    whatsapp_number = models.CharField(
        max_length=20,
        help_text='WhatsApp number with country code e.g. 919876543210',
    )
    whatsapp_message = models.CharField(
        max_length=500,
        blank=True,
        help_text='Pre-filled WhatsApp message. Leave blank to auto-generate.',
    )
    display_order = models.PositiveIntegerField(default=0)
    is_active     = models.BooleanField(default=True)

    class Meta:
        ordering            = ['display_order', 'title']
        verbose_name        = 'Career Role'
        verbose_name_plural = 'Career Roles'

    def __str__(self):
        return f"{self.department.name} — {self.title}"

    def get_whatsapp_url(self):
        """
        Returns wa.me link with pre-filled message.
        e.g. https://wa.me/919876543210?text=I+am+interested+in+Field+Staff+position
        """
        from urllib.parse import quote
        message = self.whatsapp_message or f"Hi, I am interested in the {self.title} position at TagsBikez."
        return f"https://wa.me/{self.whatsapp_number}?text={quote(message)}"