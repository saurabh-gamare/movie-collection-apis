from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken


class Register(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            raise exceptions.ValidationError({'error': serializer.errors})
        user_instance = serializer.save()
        refresh_token = RefreshToken.for_user(user_instance)
        return Response({'access_token': str(refresh_token.access_token)})

