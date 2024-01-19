from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import get_user_model

User = get_user_model()


class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Lista de rotas que não exigem autenticação
        unauthenticated_routes = ['/login/', '/create_user/', '/csrf/']

# Ignore token verification for unauthenticated routes
        if request.path in unauthenticated_routes:
            return self.get_response(request)

        header = request.META.get('HTTP_AUTHORIZATION')
        if header is None:
            return JsonResponse({'error': 'Credenciais de autenticação não foram fornecidas'}, status=401)

        header_parts = header.split()
        if len(header_parts) != 2 or header_parts[0] != 'Bearer':
            return JsonResponse({'errorElse': 'Token inválido'}, status=401)

        try:
            token = header_parts[1]
            validated_token = AccessToken(token)
            user = User.objects.get(id=validated_token['user_id'])
            request.user = {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
        except TokenError:
            return JsonResponse({'errorTry': 'Token inválido'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'errorTry': 'Usuário não encontrado'}, status=401)

        return self.get_response(request)
