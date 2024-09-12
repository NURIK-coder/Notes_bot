from rest_framework import serializers as s

from users.models import User, Role

class RoleSerialize(s.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name']
class UserCreateSerializer(s.ModelSerializer):
    role = RoleSerialize(read_only=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'password', 'role']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(user.password)
        user.role = Role.objects.get(name='user')
        user.save()
        return user

class UserSerializer(s.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'role']
