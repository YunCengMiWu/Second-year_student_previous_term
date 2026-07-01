def factorial(n):
    """计算n的阶乘（n!）"""
    result = 1
    if n == 0 or n == 1:
        return 1  # 处理n为0或1
    for i in range(2, n + 1):  # 迭代
        result *= i
    return result  # 定义计算阶乘的函数


# 计算1! + 2! + ... + 10!的总和
total = 0
for num in range(1, 11):
    total += factorial(num)  # 调用阶乘函数并累加结果
    print(f"{num}! = {factorial(num)}")  # 打印每个阶乘的结果，方便查看中间过程
print(f"1! + 2! + 3! + ... + 10! = {total}")  # 输出总和
