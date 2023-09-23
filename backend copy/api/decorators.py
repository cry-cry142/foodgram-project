from rest_framework.exceptions import MethodNotAllowed


def not_allowed_put_method(cls):
    """
    Декоратор класса.\n
    Меняет в классе метод update().
    При PUT запросе выдает ошибку 405_METHOD_NOT_ALLOWED.
    """
    upd = cls.update

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed(request.method)
        return upd(self, request, *args, **kwargs)

    cls.update = update
    return cls
