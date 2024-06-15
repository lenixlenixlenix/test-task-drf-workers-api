from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Check for token in URL query parameters
        token = request.query_params.get('token')
        if token:
            try:
                validated_token = self.get_validated_token(token)
                return self.get_user(validated_token), validated_token
            except Exception as e:
                raise AuthenticationFailed(f'Invalid token: {e}')

        return super().authenticate(request)
