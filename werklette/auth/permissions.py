from functools import wraps
from werklette.exceptions import Forbidden


SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


def permission_decorator_factory(permission_class, **permission_kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(args, **kwargs):
            perm = permission_class(**permission_kwargs)
            if not perm.has_permission():
                raise Forbidden
            return func(*args, **kwargs)
        return wrapper
    return decorator


class BasePermission:
    def has_permission(self, request):
        raise NotImplementedError


class AllowAny(BasePermission):
    def has_permission(self, request):
        return True


class IsAuthenticated(BasePermission):
    def has_permission(self, request):
        return request.user.is_authenticated


class isAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request):
        return request.method in SAFE_METHODS or request.user.is_authenticated


class IsAdmin(BasePermission):
    def has_permission(self, request):
        return request.user.is_admin


allow_any = permission_decorator_factory(AllowAny)
is_authenticated = permission_decorator_factory(IsAuthenticated)
is_authenticated_or_read_only = permission_decorator_factory(isAuthenticatedOrReadOnly)
is_admin = permission_decorator_factory(IsAdmin)