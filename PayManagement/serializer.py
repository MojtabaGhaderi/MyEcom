from rest_framework import serializers

from PayManagement.models import PaymentModel


class PaymentHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentModel
        fields = '__all__'

