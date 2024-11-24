from django import forms
from django.db import models
from django.db.models import Max

class AutoIncrementOrder(models.Model):
    order = models.PositiveIntegerField(editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.order is None:
            max_order = self.__class__.objects.filter(**self.get_filter_criteria()).aggregate(Max('order'))[
                    'order__max']
            self.order = (max_order or 0) + 1
        super().save(*args, **kwargs)

    def get_filter_criteria(self):
         raise NotImplementedError("get_filter ERROR/common")




class DisableFieldsMixin(forms.Form):
    disabled_fields = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if self.disabled_fields[0] == '__all__' or field_name in self.disabled_fields:
                field.disabled = True