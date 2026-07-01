odd_sum = 0  # 初始化奇数和
even_sum = 0  # 初始化偶数和

# 遍历1到50的所有数字
for num in range(1, 51):
    if num % 2 == 0:
        even_sum += num  # 累加偶数
    else:
        odd_sum += num  # 累加奇数
print(f"1-50内所有奇数的和为: {odd_sum}")
print(f"1-50内所有偶数的和为: {even_sum}")
