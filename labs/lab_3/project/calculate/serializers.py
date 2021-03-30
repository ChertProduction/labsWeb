from rest_framework import serializers


class CalculationRequestSerializer(serializers.Serializer):
    input_value = serializers.FloatField(min_value=0)

class CalculationResponseSerializer(serializers.Serializer):
    output_value = serializers.FloatField(min_value=0)