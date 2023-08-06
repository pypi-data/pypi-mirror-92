from functools import wraps

from skyext import EXT_CONTEXT


def db_session_decorator(func):
    @wraps(func)
    def inner(self, **kwargs):
        print('db session before...........')
        with EXT_CONTEXT["db"].session_maker() as session:
            kwargs["db_session"] = session
            res = func(self, **kwargs)

        print('db session after............')
        return res
    return inner