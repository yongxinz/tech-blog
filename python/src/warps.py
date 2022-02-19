import time


def funA():
    start = time.time()
    for i in range(1000000):
        pass
    end = time.time()

    print("funA cost time = {}".format(end-start))


def warps():
    def warp(func):
        def _warp(*args, **kwargs):
            start = time.time()
            func(*args, **kwargs)
            end = time.time()
            print("{} cost time = {}".format(getattr(func, '__name__'), (end-start)))
        return _warp
    return warp


@warps()
def funB():
    # start = time.time()
    for i in range(2000000):
        pass
    # end = time.time()

    # print("funB cost time = %f s" % (end-start))


if __name__ == '__main__':
    funB()
