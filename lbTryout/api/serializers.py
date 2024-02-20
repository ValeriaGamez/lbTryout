from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Par

class ParSerializer(serializers.ModelSerializer):
    swimTime = serializers.DurationField()
    rsrTime = serializers.DurationField()

    class Meta:
        model = Par
        fields = '__all__'
