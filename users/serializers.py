from rest_framework import serializers
from .models import User, Address, Ticket


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}
        depth = 2


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    mobile = serializers.CharField()
    password = serializers.CharField()
    password_confirmation = serializers.CharField()

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError(
                'password confirmation is not true.')
        return attrs


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['text', "lat", "long",
                  "create_date_time", "modify_date_time"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        address = Address(**validated_data)
        address.user = self.context['request'].user
        address.save()
        return address


class UserFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'mobile', 'birth_date', 'city',
                  'national_code', 'description', 'gender']

    # def update(self, instance, validated_data):
    #     instance.


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        ticket = Ticket(**validated_data)
        ticket.user = self.context['request'].user
        ticket.save()
        return ticket
