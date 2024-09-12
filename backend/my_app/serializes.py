from rest_framework import serializers

from my_app.models import Note
from users.models import User, Role


# class NotesSerializer(serializers.Serializer):
#     title = serializers.CharField(allow_null=True)
#     description = serializers.CharField(allow_null=True)



class RoleSerializeView(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name']

class UserSerializerView(serializers.ModelSerializer):
    role = RoleSerializeView(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'role']

class NoteSerializer(serializers.ModelSerializer):
    # description = serializers.CharField(write_only=True) #переопределение Когда serializers.Serializer
    user_id = UserSerializerView(read_only=True)
    class Meta:
        model = Note
        fields = ['id', 'title', 'description', 'created_at', 'status', 'user_id']
        # extra_kwargs = {
        #     'description': {
        #         'write_only': True
        #     }
        # }#переопределение Когда serializers.ModelSerializer

class NotesCreateSerialize(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'description', 'status', 'user_id']

