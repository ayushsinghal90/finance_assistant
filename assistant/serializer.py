from rest_framework import serializers
from .models import FinancialInfo


class FinancialInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialInfo
        fields = ['id', 'assets', 'expenditures', 'income', 'summary']