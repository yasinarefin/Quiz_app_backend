from rest_framework.response import  Response
from rest_framework.decorators import api_view
from rest_framework import status
from User import serializers, models
from Authentication import security_tools as st


'''
this is login endpoint.
Data format in the  endpoint
{
    "email" : "name@domain.com",
    "password" : "password"
}

if credentials are correct
HTTP_200
{
    "token" : "sometoken"
}

HTTP 401 otherwise
'''

@api_view(['POST'])
def login(request):
    credentials = request.data
    email = credentials['email']
    password = credentials['password']
    
    login_status, token = st.login(email, password)

    # return token if login successfull
    if login_status == True:
        return Response({'token' : token}, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_401_UNAUTHORIZED)


'''
to delete token use this endpoint 
{
    "token" : "current_token"
}

if successfull HTTP_200
otherwise HTTP_400
'''
@api_view(['POST'])
def logout(request):
    token = request.data['token']

    if st.logout(token):
        return Response(status=status.HTTP_200_OK)
    return  Response(status=status.HTTP_400_BAD_REQUEST)