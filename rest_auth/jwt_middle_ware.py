import jwt
from viit import settings
from django.http import JsonResponse

class JWTAuthentication(object):

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'token':
            return None
        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid  characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, payload):

        decoded_dict = jws.verify(payload, settings.SECRET_KEY)

        username = decoded_dict.get('username', None)
        expiry = decoded_dict.get('expiry', None)

        try:
            usr = User.objects.get(username=username)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not usr.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        if expiry < datetime.date.today():
            raise exceptions.AuthenticationFailed(_('Token Expired.'))

        return (usr, payload)

    def authenticate_header(self, request):
        return 'Token'
