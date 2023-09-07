def segement_print(func):
    def inner(*args):
        print("-" * 30)
        res = func(*args)
        print("-" * 30)
        return res

    return inner
