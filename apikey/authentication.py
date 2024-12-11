from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import APIKey  # Import your APIKey model


class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('X-API-Key')  # Look for the API key in the request headers
        if not api_key:
            raise AuthenticationFailed("No API key provided")

        try:
            APIKey.objects.get(key=api_key)  # Validate the API key
        except APIKey.DoesNotExist:
            raise AuthenticationFailed("Invalid API key")

        # Return (user, None) because DRF expects a user instance, but we're not tying this to a user
        return (None, None)
