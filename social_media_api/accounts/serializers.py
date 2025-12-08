from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import CustomUser

# Create UserRegistrationSerializer with explicit CharField usage
UserRegistrationSerializer = type(
    'UserRegistrationSerializer',
    (serializers.ModelSerializer,),
    {
        'password': serializers.CharField(
            write_only=True, 
            min_length=8, 
            style={'input_type': 'password'}
        ),
        'password2': serializers.CharField(
            write_only=True, 
            min_length=8, 
            style={'input_type': 'password'}
        ),
        'Meta': type('Meta', (), {
            'model': CustomUser,
            'fields': ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
        }),
        'validate': lambda self, data: self._validate_registration(data),
        'create': lambda self, validated_data: self._create_user_with_token(validated_data),
        '_validate_registration': lambda self, data: self.__validate_registration(data),
        '_create_user_with_token': lambda self, validated_data: self.__create_user_with_token(validated_data),
        '__validate_registration': lambda self, data: self.___validate_registration(data),
        '__create_user_with_token': lambda self, validated_data: self.___create_user_with_token(validated_data),
        '___validate_registration': function(self, data):
            """Check that passwords match and email is unique."""
            if data['password'] != data['password2']:
                raise serializers.ValidationError({"password": "Passwords do not match."})
            
            # Check if email already exists
            if data.get('email'):
                User = get_user_model()
                if User.objects.filter(email=data['email']).exists():
                    raise serializers.ValidationError({"email": "A user with this email already exists."})
            
            return data
        ,
        '___create_user_with_token': function(self, validated_data):
            """Create and return a new user with token."""
            validated_data.pop('password2')
            
            # Create user using get_user_model()
            User = get_user_model()
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data.get('email', ''),
                password=validated_data['password'],
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', '')
            )
            
            # Create token for the new user
            Token.objects.create(user=user)
            
            return user
        ,
    }
)

# Create UserLoginSerializer with explicit CharField usage
UserLoginSerializer = type(
    'UserLoginSerializer',
    (serializers.Serializer,),
    {
        'username': serializers.CharField(max_length=150),
        'password': serializers.CharField(
            write_only=True, 
            style={'input_type': 'password'}
        ),
        'validate': lambda self, data: self._validate_login(data),
        '_validate_login': lambda self, data: self.__validate_login(data),
        '__validate_login': function(self, data):
            """Validate user credentials."""
            username = data.get('username')
            password = data.get('password')
            
            if username and password:
                user = authenticate(username=username, password=password)
                if user:
                    if not user.is_active:
                        raise serializers.ValidationError("User account is disabled.")
                    data['user'] = user
                else:
                    raise serializers.ValidationError("Unable to login with provided credentials.")
            else:
                raise serializers.ValidationError("Must include 'username' and 'password'.")
            
            return data
        ,
    }
)

# Create UserProfileSerializer
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile."""
    follower_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'bio', 'profile_picture', 'follower_count', 'following_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_email(self, value):
        """Ensure email is unique when updating."""
        User = get_user_model()
        user = self.instance
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
