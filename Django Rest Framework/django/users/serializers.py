from rest_framework import serializers
from users.models import NewUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = NewUser
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this otherwise we use another technique in TraverseMedia
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class RegisterUserSerializer(serializers.ModelSerializer):
    

    # Need to do this when have to specify fields explicitly, mostly done to override default fields

    # email = serializers.EmailField(required=True)
    # username = serializers.CharField(required=True)
    # password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = NewUser
        fields = ('email', 'username', 'password')
        # For fields with extra arguments such as password for security purposes, maybe cant copy password
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # On creation we validate the password
        password = validated_data.pop('password', None) # If password not there then Pop None
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

        # Otherweise

        # user = NewUser(
        #     email = validated_data['email'],
        #     username = validated_data['username']
        # )
        # user.set_password(validated_data['password'])
        # user.save()
        # return user