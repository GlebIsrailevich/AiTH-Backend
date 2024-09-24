def factorial_f(n:int)->int:
    if n < 0:
        raise 
    assert type(n) == int
    n_val = 1
    for num in range(1, n + 1):
        n_val *= num
    return n_val
    


def fibbonacci_f(n:int)->float:
    if n < 0:
        raise
    fibbs = []
    for num in range(n+1):
        if num < 2:
            fibbs.append(num)
        else:
            n_val = (fibbs[-1]) + (fibbs[-2])
            fibbs.append(n_val)
    return fibbs[-1]

def mean_f(n)->float:
    if len(n) == 0:
        raise Exception
    n_len = 0
    n_sum = 0
    for num in range(len(n)):
        n_len += 1
        n_sum += n[num]
    return n_sum/n_len