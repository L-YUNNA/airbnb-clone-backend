from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User

class TrustMeBroAuthentication(BaseAuthentication):

    def authenticate(self, request): 
        username = request.headers.get('Trust-Me')
        if not username:    # 2.
            return None
        try:
            user = User.objects.get(username=username)
            return (user, None)  # 3. 
        except User.DoesNotExist:  # 1.
            raise AuthenticationFailed(f"No user {username}")



