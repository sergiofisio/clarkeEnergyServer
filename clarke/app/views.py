from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import User


@permission_classes([AllowAny])
@api_view(['POST'])
def create_user(request):
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')

    if not all([name, email, password]):
        return Response({'error': 'Todos os campos são obrigatórios'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email já cadastrado'}, status=status.HTTP_409_CONFLICT)

    hashed_password = make_password(password)
    user = User(name=name, email=email, password=hashed_password)
    user.save()

    return Response({'message': 'Usuário criado com sucesso'}, status=status.HTTP_201_CREATED)


@csrf_exempt
@permission_classes([AllowAny])
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, username=email, password=password)

    if user is None:
        return Response({'error': 'Email ou senha inválidos'}, status=status.HTTP_401_UNAUTHORIZED)
    print('user', user)
    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'token': str(refresh.access_token),
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email,
        }})


@ensure_csrf_cookie
@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_token(request):
    return Response({})


@api_view(['GET'])
def get_users(request):
    # ou quaisquer campos que você queira
    print('request.user', request.user.id)
    users = User.objects.all().values('id', 'email', 'password')
    return Response(users)
