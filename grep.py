def grep(pattern):
    print("Looking for {pattern}".format(pattern=pattern))
    while True:
        line = (yield)
        if pattern in line:
            print(line)

def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr
    return start
