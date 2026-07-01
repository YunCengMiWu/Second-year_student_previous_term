# 数值与进制转换程序
# 输入一个自然数，输出其二进制、八进制、十六进制形式

# 获取用户输入的自然数
try:
    num = int(input("请输入一个自然数: "))

    # 检查是否为自然数
    if num < 0:
        print("请输入一个非负整数！")
    else:
        # 进行进制转换
        binary = bin(num)  # 二进制，结果以'0b'开头
        octal = oct(num)  # 八进制，结果以'0o'开头
        hexadecimal = hex(num)  # 十六进制，结果以'0x'开头

        # 输出转换结果
        print(f"\n十进制数 {num} 的各种进制表示:")
        print(f"二进制: {binary}")
        print(f"八进制: {octal}")
        print(f"十六进制: {hexadecimal}")

        # 额外输出不带前缀的形式
        print("\n不带前缀的表示:")
        print(f"二进制: {binary[2:]}")
        print(f"八进制: {octal[2:]}")
        print(f"十六进制: {hexadecimal[2:].upper()}")  # 十六进制通常用大写字母表示

except ValueError:
    print("输入错误！请输入一个有效的自然数。")
