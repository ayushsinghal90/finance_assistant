from django.db import models
from django.core.serializers.json import DjangoJSONEncoder


class FinancialInfo(models.Model):
    assets = models.JSONField(encoder=DjangoJSONEncoder, default=dict)
    expenditures = models.JSONField(encoder=DjangoJSONEncoder, default=dict)
    income = models.JSONField(encoder=DjangoJSONEncoder, default=dict)
    summary = models.JSONField(encoder=DjangoJSONEncoder, default=dict)

    def __str__(self):
        return f"Financial Info {self.id}"
