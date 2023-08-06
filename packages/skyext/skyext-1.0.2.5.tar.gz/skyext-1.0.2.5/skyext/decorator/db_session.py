from functools import wraps

from skyext import db


def db_session_decorator(func):
    @wraps(func)
    def inner(self, **kwargs):
        with db.session as session:
            kwargs["db_session"] = session
            res = func(self, **kwargs)
        return res

    return inner