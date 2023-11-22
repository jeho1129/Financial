from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import UserInfoSerializer, UserChangeSerializer


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def userinfo(request):
    Usermodel = get_user_model()
    user = Usermodel.objects.get(pk=request.user.pk)
    if request.method == 'GET':
        serializer = UserInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = UserChangeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            if 'password1' in request.data:
                if request.data['password1'] == request.data['password2']:
                    user.set_password(request.data['password1'])
                    update_session_auth_hash(request, user)
                else:
                    return Response({'message': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)