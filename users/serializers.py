from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.db import transaction


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    group = serializers.ChoiceField(choices=['Manager', 'Employee'], write_only=True)

    class Meta:
        model = User
        fields = ['username', 'group', 'email', 'password']

    @transaction.atomic
    def create(self, validated_data):
        group_name = validated_data.pop('group')

        try:
            group = Group.objects.get(name=group_name)
        except:
            return serializers.ValidationError({"group": "Group does not available. Please select Manager or Employee."})

        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        user.groups.add(group)
        return user