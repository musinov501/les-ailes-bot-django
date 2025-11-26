from django.db import models
from django.utils.translation import gettext as _
from bot.models.base import BaseModel, City

class Branch(BaseModel):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    opening_hours = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='branches')
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    
    
    def __str__(self):
        return self.name
    
    
    class Meta:
        db_table = 'branch'
        verbose_name = _("Branch")
        verbose_name_plural = _("Branches")