print("所有的水仙花数（3位数）有：")


for num in range(100, 1000):  # 遍历所有3位数（100到999）

    hundreds = num // 100  # 分解出百位数字

    tens = (num // 10) % 10  # 分解出十位数字

    units = num % 10  # 分解出个位数字

    sum_of_cubes = hundreds**3 + tens**3 + units**3  # 计算每个位上的数字的3次幂之和

    # 判断
    if sum_of_cubes == num:
        print(num)
