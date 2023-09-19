from rest_framework.serializers import ModelSerializer
from .models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','password']
        extra_kwargs = {
            #extra property for name parameter , write_only means the password is write but can not be read - no return in the result
            'password':{'write_only':True}
        }
    
    #create will be called when serializer = UserSerializer(data=data)
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password) #hash the password
        instance.save()
        return instance
