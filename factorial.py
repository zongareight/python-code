def fact(n):
    if n <= 0:
        return 1
    a = n * fact(n - 1)
    return a


if __name__ == '__main__':
    n = input('Введите целое число: ')
    while not n.isdigit():
        print(f'{n} не является целым числом.')
        n = input('Повторите ввод: ')
    n = int(n)
    print(f'{n}! = {fact(n)}')
