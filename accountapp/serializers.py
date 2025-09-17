import re
from rest_framework import serializers
from .models import  User

# 1. User Serializer
class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'role', 'password', 'password_confirm'
        ]
        extra_kwargs = {                
            'password': {'write_only': True}            # DRF will not include the password in any GET response.
        }

    # Custom validation for email ending with a specific domain
    def validate_email(self, value):
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError("Only '@gmail.com' emails are allowed.")
        return value

    def validate_username(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("Username must be at least 4 characters long.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        return value
  
    def validate(self, data):
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError("Passwords do not match.")
        if data['first_name'].lower() == data['last_name'].lower():
            raise serializers.ValidationError("First name and last name cannot be the same.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')                  # password_confirm is not a field in the model
        password = validated_data.pop('password')               # We cannot save password directly, it needs to be hashed
        user = User(**validated_data)                           # Create a new User instance
        user.set_password(password)                             # Hash the password        
        user.save()                                             # Save the user instance     
        return user
