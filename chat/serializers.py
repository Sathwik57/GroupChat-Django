import string
from attr import fields
from django.contrib.auth import get_user_model
from rest_framework import serializers 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from chat.models import Group


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True, 
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True, 
        style={'input_type': 'password'}
    )

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password1', 'password2']
        read_only_fields = ['id',]

    def validate(self, attrs):
        pswd1, pswd2 = attrs.get('password1') , attrs.get('password2')
        if len(pswd1) < 8:
            raise serializers.ValidationError("Password must be atleast 8 characters") 
        elif pswd1 != pswd2 :
            raise serializers.ValidationError("Both Passwords must match")
        elif not [1 for x in pswd1 if x in string.ascii_uppercase]:
            raise serializers.ValidationError("Password must have atleast 1 Upper case")
        else:                
            return attrs
    
    def create(self, validated_data):
        data = {
            key: value for key, value in validated_data.items()
            if key not in ('password1', 'password2')
        }
        data['password'] = validated_data['password1']
        return self.Meta.model.objects.create_user(**data)


class CUser(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id',]


class LogInSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = UserSerializer(user).data
        for key, value in user_data.items():
            if key != 'id':
                token[key] = value
        return token


class GroupSerializer(serializers.ModelSerializer):
    members = UserSerializer
    chat_url = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ['admin','slug',]

    def save(self, **kwargs):
        try:
            user = self.context['request'].user
            assert isinstance(user, get_user_model())
        except:
            raise serializers.ValidationError("Not authenticated")
        self.validated_data['admin'] = user
        _members = self.validated_data.pop('members')
        obj = super().save(**kwargs)
        if not user in obj.members.all():
            _members.append(user)
        [obj.members.add(member) for member in _members]
        obj.save()
        return obj


    def get_chat_url(self,obj):
        return f'ws://chat/{obj.slug}'