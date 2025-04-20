import re
from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    def validate_cpf_cnpj(self, value):
        digits = re.sub(r'\D', '', value)
        if len(digits) not in (11, 14):
            raise serializers.ValidationError(
                "O CPF deve ter 11 dígitos e o CNPJ 14 dígitos."
            )
        return value
    
    def validate(self, attrs):
        # attrs é um dict com todos os campos já validados
        if attrs.get('is_blocked') and attrs.get('qtd_seller', 0) > 0:
            raise serializers.ValidationError(
                "Cliente bloqueado não pode ter vendedores ativos."
            )
        return attrs
