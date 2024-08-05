from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.hashers import make_password

from .validators import validate_file_extension
from .serializers import SignUpSerializer, UserSerializer

from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User

from django.http import FileResponse

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode


# Create your views here.

""" @api_view(['POST'])
def register(request):
    data = request.data

    user = SignUpSerializer(data=data)

    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():
           user = User.objects.create(
               first_name = data['first_name'],
               last_name = data['last_name'],
               username = data['email'],
               email = data['email'],
               password = make_password(data['password'])
           ) 

           return Response({
                'message': 'User registered.'},
                status=status.HTTP_200_OK
            )
        else:
            return Response({
                'error': 'User already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

    else:
        return Response(user.errors)
 """

@api_view(['POST'])
def register(request):
    data = request.data

    serializer = SignUpSerializer(data=data)

    if serializer.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            serializer.save()

            return Response({
                'message': 'User registered.'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'User already exists.'
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def currentUser(request):

    user = UserSerializer(request.user)

    return Response(user.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request):
    user = request.user

    data = request.data    

    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.username = data['email']
    user.email = data['email']

    if data['password'] != '':
        user.password = make_password(data['password'])

    user.save()

    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def uploadResume(request):

    user = request.user
    resume = request.FILES['resume']

    if resume == '':
        return Response({ 'error': 'Please upload your resume.' }, status=status.HTTP_400_BAD_REQUEST)

    isValidFile = validate_file_extension(resume.name)

    if not isValidFile:
        return Response({ 'error': 'Please upload only pdf file.' }, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(user, many=False)

    user.userprofile.resume = resume
    user.userprofile.save()

    return Response(serializer.data)

@api_view(['POST'])
def resetPassword(request):
    try:
        # Get email and new password from request
        email = request.data.get('email')
        new_password = request.data.get('new_password', '')

        # Find user by email
        user = User.objects.get(email=email)
        if user:
            # Update password
            user.set_password(new_password)
            user.save()

            return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error':'No user found with this email'})

    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': 'No user found with this email'})


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def serve_resume(request):
#     user = request.user
#     resume = user.userprofile.resume
#     if resume:
#         response = FileResponse(resume)
#         return response
#     else:
#         return Response({'error': 'No resume found for this user.'}, status=status.HTTP_404_NOT_FOUND)

