from rest_framework.serializers import *
from .models import Students
from rest_framework.serializers import CharField as CF,IntegerField as IF,FileField as FF

class StudentSer(ModelSerializer):
    class Meta:
        model=Students
        fields='__all__'

class StudentCreateSerializer(Serializer):
    first_name=CF(required=0)
    last_name=CF(required=True)
    course=CF(required=True)
    image=FF(required=False)
    def create(self,validated_data):
        return Students.objects.create(**validated_data)

class StudenUpdateSerializer(Serializer):
    first_name=CF(required=False)
    last_name=CF(required=False)
    enrollment_no=IF(required=False)
    course=CF(required=False)
    image=FF(required=False)

    def validate(self,data):
        return data

    def update(self,instance,validated_data):

        instance.first_name=validated_data.get('first_name',instance.first_name)
        instance.enrollment_no=validated_data.get('enrollment_no',instance.enrollment_no)
        instance.course=validated_data.get('course',instance.course)
        instance.image=validated_data.get('image',instance.image)
        instance.save()
        return validated_data