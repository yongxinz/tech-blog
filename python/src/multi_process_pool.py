from multiprocessing import Pool, Manager


def func(my_list, my_dict):
    my_list.append(10)
    my_list.append(11)
    my_dict['a'] = 1
    my_dict['b'] = 2


if __name__ == '__main__':
    manager = Manager()
    my_list = manager.list()
    my_dict = manager.dict()

    pool = Pool(processes=2)
    for i in range(0, 2):
        pool.apply_async(func, (my_list, my_dict))
    pool.close()
    pool.join()

    print(my_list)
    print(my_dict)
