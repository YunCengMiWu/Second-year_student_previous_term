# 程序1：计算自然数各位数字之和
print("===== 程序1：计算自然数各位数字之和 =====")
num = input("请输入一个任意大的自然数：")  # 获取输入的自然数
print(f"各位数字之和为：{sum(map(int, num))}\n")

# 程序2：计算三角形面积
print("===== 程序2：计算三角形面积 =====")
from math import sqrt  # 导入平方根函数

# 获取三角形三边长
a, b, c = input("请输入三角形的三边长（用空格分隔）：").split()
a, b, c = int(a), int(b), int(c)  # 转换为整数
s = (a + b + c) / 2  # 计算半周长
area = sqrt(s * (s - a) * (s - b) * (s - c))  # 应用海伦公式
print(f"三角形面积为：{area:.6f}\n")

# 程序3：用while计算1到100的总和
print("===== 程序3：计算1到100的总和 =====")
total = 0  # 初始化总和
i = 1  # 初始化计数器
while i <= 100:
    total += i  # 累加当前数字
    i += 1  # 计数器自增
print(f"1到100的总和是：{total}")
