from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import UserInfoSerializer, UserChangeSerializer

# Create your views here.
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def userinfo(request):
    Usermodel = get_user_model()
    user = Usermodel.objects.get(pk=request.user.pk)
    if request.method == 'GET':
        serializer = UserInfoSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserChangeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)