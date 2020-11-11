

def main():
    list_a = [1, 2, 3, 4, 5]
    list_b = [4, 5, 6, 7, 8]

    # 求交集的两种方式
    res_a = [i for i in list_a if i in list_b]
    res_b = list(set(list_a).intersection(set(list_b)))

    print(f"res_a is: {res_a}")
    print(f"res_b is: {res_b}")

    # 求并集
    res_c = list(set(list_a).union(set(list_b)))
    print(f"res_c is: {res_c}")

    # 求差集的两种方式，在B中但不在A中
    res_d = [i for i in list_b if i not in list_a]
    res_e = list(set(list_b).difference(set(list_a)))

    print(f"res_d is: {res_d}")
    print(f"res_e is: {res_e}")


if __name__ == '__main__':
    main()
