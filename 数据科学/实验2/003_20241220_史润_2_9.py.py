numbers = [1, 5, 8, -17, 15, 25, 78, -5, 36, 50, 40]  # 创建初始列表
A = sum(numbers[0:5])  # 计算列表中前5个数的和，记为A
B = sum(numbers[-5:])  # 计算列表中最后5个数的和，记为B
total = A + B
numbers.append(total)  # 将结果附加到列表末尾

print(f"A（前5个数的和）: {A}")
print(f"B（最后5个数的和）: {B}")
print(f"A + B: {total}")
print("最终列表：", numbers)
