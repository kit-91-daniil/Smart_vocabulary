def summary(x: int) -> int:
    global y
    y = 23
    x_str = str(x)
    result_list = [int(i) for i in x_str]
    return sum(result_list)


print(summary(12345))
print(y)
