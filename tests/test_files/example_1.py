import sys


def func_1(val):
    print(val)


def func_2(val):
    func_1(val)


def func_3(val):
    func_2(val)


def func_4(val=4):
    return func_3(val)


if __name__ == "__main__":
    func_4()
