from rest_framework import serializers
from .models import BPRecord

class BPRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPRecord
        fields = ['patient_id', 'systolic', 'diastolic', 'created_at']
