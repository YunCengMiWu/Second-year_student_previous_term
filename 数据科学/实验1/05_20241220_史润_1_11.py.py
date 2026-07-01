# 1. 打印输出
print("Hello, World!")
# 2. 变量类型和声明
count = 10
average = 89.5
grade = "A"
name = "Alice"
is_passed = True
print("count:", count)
print("average:", average)
print("grade", grade)
print("name", name)
print("passed", is_passed)
# 变量类型的动态变化
variable = 42  # 初始赋值为整数
print(variable, type(variable))
variable = 42.0  # 重新赋值为浮点数
print(variable, type(variable))

# 3. 循环结构
# for循环
for i in range(5):
    print("Number:", i)
# while循环
i = 0
while i < 5:
    print("Number:", i)
    i += 1
# 迭代字符串
text = "hello"
for char in text:
    print(char)
# 迭代列表
numbers = [10, 20, 30, 40, 50]
for number in numbers:
    print("Number:", number)
# 4. 数组和列表
numbers = [1, 2, 3, 4, 5]  # 定义
for i, number in enumerate(numbers):
    print(f"Element {i}:{number}")  # 遍历
numbers.append(6)  # 添加
del numbers[2]  # 删除
numbers.insert(2, 7)  # 插入
print("Updated List:", numbers)  # 输出


# 5. 函数定义
def add(a, b):
    return a + b


total_sum = add(5, 3)
print("sum:", sum)


def greet(name, message="Hello"):  # 带默认值的
    print(f"{message},{name}!")


greet("Alice")
greet("Bob", "Welcome")


def sum_all(*args):  # 带有可变参数的函数
    total = sum(args)
    print("Total:", total)


sum_all(1, 2, 3, 4, 5)
