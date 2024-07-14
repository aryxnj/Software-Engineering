def UnsafeApplication(func):
    def wrapper(*args, **kwargs):
        for key in args:
            if key == 0:
                raise ValueError("Error: Invalid key detected (1)")
        result = func(*args, **kwargs)
        return result

    return wrapper
