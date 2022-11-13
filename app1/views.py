from rest_framework.views import APIView
from rest_framework.response import Response
from .authentication import ExpiringTokenAuthentication
from .serializers import *
from rest_framework.permissions import *
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import datetime
import pytz

# Create your views here.

class Register(APIView):
    permission_classes=[IsAdminUser]
    def post(self,request,*args,**kwargs):
        Serializer=RegisterSer(data=request.data)
        user=request.data.get('username')
        if Serializer.is_valid(raise_exception=True):
            Serializer.save()
            User.objects.filter(username=user).update(is_staff=True)
            return Response({'message':'A staff user created successfully','data':Serializer.data},200)
        return Response({'message':'something went wrong...'},400)


class Login(APIView):
    def post(self,request,*args,**kwargs):
        username=request.data.get('username')
        password=request.data.get('password')
        qs=authenticate(username=username,password=password)
        if not qs:
            return Response({'message':"User not found"},400)
        else:
            utc_now=datetime.datetime.utcnow()
            utc_now=utc_now.replace(tzinfo=pytz.utc)
            Token.objects.filter(user=qs,created__lt=utc_now-datetime.timedelta(minutes=60)).delete()
            token , _ =Token.objects.get_or_create(user=qs)
            token.save()
            data={'username':qs.username,'token':token.key}
            return Response({'data':data},200)


class StudentsCRUD(APIView):

    permission_classes=[IsAuthenticated]
    authentication_classes=[ExpiringTokenAuthentication]

    def get(self,request,*args,**kwargs):
        try:
            qs=Students.objects.get(id=kwargs.get('pk'))
            Serializer=StudentSer(qs,context={'request':request})
            return Response({'message':'data retrived successfully','data':Serializer.data},200)
        except Exception as e:
            return Response({'message':[str(e)]},400)

    def post(self,request):
        serializer=StudentCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':'Student created successfully','data':serializer.data},200)
        return Response({'message':'Student created unsuccessfully'},400)
    

    def put(self, request, *args, **kwargs):
        try:
            utc_now=datetime.datetime.utcnow()
            utc_now=utc_now.replace(tzinfo=pytz.utc)

            instance = Students.objects.get(id=self.kwargs.get('pk'))

            if Students.objects.filter(id=instance.id,dateTime__lt=utc_now-datetime.timedelta(days=1)):
                instance.dateTime=utc_now
                instance.count=0
                instance.save()
            # instance.dateTime=utc_now
            instance.count=instance.count+1
            instance.save()

            # print(instance.dateTime)
            # print(utc_now-instance.dateTime)
            # print(utc_now)
            if 'last_name' in request.data and instance.count>4:
                instance.last_name=instance.last_name
                instance.save()
            elif 'last_name' in request.data and instance.count<=4:
                instance.last_name=request.data.get('last_name')
                instance.save()
        except:
            return Response({'message': 'Invalid student or does not exists.'}, status=400)
        serializer = StudenUpdateSerializer(data=request.data, instance=instance, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Student  data Updated Successfully'}, status=200)
        return Response(serializer.errors, status=400)


    def delete(self,request,*args,**kwargs):
        try:
            Students.objects.get(id=self.kwargs.get('pk')).delete()
            return Response({'message':'Deleted successfully'},200)
        except:
            return Response({'message':'Student does not exist'},400)
