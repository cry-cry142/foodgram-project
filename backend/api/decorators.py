from rest_framework import status
from rest_framework.response import Response


def not_allowed_put_method(cls):
    """
    Декоратор класса.\n
    Меняет в классе метод update().
    При PUT запросе выдает ошибку 405_METHOD_NOT_ALLOWED.
    """
    upd = cls.update

    def update(self, request, *args, **kwargs):
        if self.action == 'update':
            response = {'detail': 'Method \"PUT\" not allowed.'}
            return Response(
                response, status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return upd(self, request, *args, **kwargs)

    cls.update = update
    return cls
