def segement_print(func):
    def inner(*args):
        print("-" * 20)
        res = func(*args)
        print("-" * 20)
        return res

    return inner
