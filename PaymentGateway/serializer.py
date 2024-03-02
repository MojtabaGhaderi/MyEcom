from rest_framework import serializers

from PaymentGateway.models import PaymentModel


class PaymentHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentModel
        fields = '__all__'

