from rest_framework import serializers
from .models import RealUser

class RealUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealUser
        fields = '__all__'