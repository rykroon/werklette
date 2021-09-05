from base64 import  b64decode


class BaseUser:
    @property
    def identifier(self):
        raise NotImplementedError

    @property
    def is_authenticated(self):
        raise NotImplementedError

    @property
    def is_admin(self):
        raise NotImplementedError


class SimpleUser(BaseUser):
    def __init__(self, username):
        self.username = username

    @property
    def identifier(self):
        return self.username

    @property
    def is_authenticated(self):
        return True


class AnonymousUser(BaseUser):

    def __init__(self, ip_address):
        self.ip_address = ip_address

    @property
    def identifier(self):
        return self.ip_address

    @property
    def is_authenticated(self):
        return False


class BaseAuthentication:

    def authenticate(self, request):
        raise NotImplementedError


class SchemeAuthentication(BaseAuthentication):
    scheme = ''

    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return

        scheme, _, credentials = authorization_header.partition(' ')
        if scheme.lower() != self.scheme.lower():
            return

        return self.validate_credentials(credentials)

    def validate_credentials(self, credentials):
        raise NotImplementedError


class BasicAuthentication(SchemeAuthentication):
    scheme = 'basic'

    def validate_credentials(self, credentials):
        decoded_credentials = b64decode(credentials)
        username, _, password = decoded_credentials.partition(':')
        return self.validate_user(username, password)

    def validate_user(self, username, password):
        raise NotImplementedError


class BearerAuthentication(SchemeAuthentication):
    scheme = 'bearer'

