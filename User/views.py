from rest_framework.response import  Response
from rest_framework.decorators import api_view
from User import serializers, models
from User.serializers import UserViewSerializer
from User.models import  User as  CustomUser
from Authentication.models import  Token
from rest_framework import status

# Create your views here.

'''
if user creation successfull returns HTTP_201
else HTTP_400
uses UserCreateSerializer
'''
@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        print(request.data['email'])
        try:
            CustomUser.objects.get(email=request.data['email'])
            return Response({'message':'Email already exists!'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass
        try:
            CustomUser.objects.get(user_name=request.data['user_name']) 
            return Response({'message':'Username already exists!'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass

        userS = serializers.UserCreateSerializer(data = request.data)
        
        if  userS.is_valid():
            userS.save()
            return Response({'message' : 'user created succesfully.'},status=status.HTTP_201_CREATED)
        else:
            return Response({'message' : 'invalid data'},status=status.HTTP_400_BAD_REQUEST)

'''
get user details 
needs auth token to access
returns HTTP_401 if failed.
else HTTP_200
'''
@api_view(['GET'])
def get_user(request):
    if request.method == 'GET':
        headers = request.headers
        token = headers['Authorization']

        try:
            user = Token.objects.get(token= token)
            us = UserViewSerializer(CustomUser.objects.get(email=user.user))
            return Response(us.data, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        