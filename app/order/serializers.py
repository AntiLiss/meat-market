from rest_framework import serializers

class OrderSerializer(serializers.ModelSerializer):
    """Order serializer"""
    
    class Meta:
        fields = ('id', 'user', 'shipping_address', 'total', 'is_paid')