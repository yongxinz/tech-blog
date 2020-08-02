import multiprocessing


def func(num):
    # 共享数值型变量
    # num.value = 10.78

    # 共享数组型变量
    num[2] = 9999


if __name__ == '__main__':
    # 共享数值型变量
    # num = multiprocessing.Value('d', 10.0)
    # print(num.value)

    # 共享数组型变量
    num = multiprocessing.Array('i', [1, 2, 3, 4, 5])
    print(num[:])

    p = multiprocessing.Process(target=func, args=(num,))
    p.start()
    p.join()

    # 共享数值型变量
    # print(num.value)

    # 共享数组型变量
    print(num[:])
