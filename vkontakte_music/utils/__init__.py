


def apply(call):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return call(func(*args, **kwargs))
        return wrapper
    return decorator