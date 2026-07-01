import copy

original = [
    100,  # 不可变对象（数字）
    "hello",  # 不可变对象（字符串）
    (1, 2, 3),  # 不可变对象（元组）
    [4, 5, 6],  # 可变对象（列表）
    {"a": 7, "b": 8},  # 可变对象（字典）
]  # 创建一个包含多种数据类型的嵌套列表

assigned = original  # 使用赋值创建新变量
copied = copy.copy(original)  # 使用浅拷贝创建新变量
print("=== 修改前 ===")
print("原始列表:", original)
print("赋值得到的列表:", assigned)
print("浅拷贝得到的列表:", copied)
print("原始与赋值的内存地址是否相同:", original is assigned)
print("原始与拷贝的内存地址是否相同:", original is copied)
print()


print("=== 修改原始列表中的元素 ===")

original[0] = 200  # 修改不可变元素数字（会创建新对象）
original[1] = "world"  # 修改不可变元素字符串（会创建新对象）

original[3].append(7)  # 修改可变元素列表
original[4]["c"] = 9  # 修改可变元素字典
print("修改后的原始列表:", original)
print("赋值得到的列表（assigned）的变化:", assigned)
print("浅拷贝得到的列表（copied）的变化:", copied)
print()
print("=== 结论分析 ===")
print("1. 赋值操作(=)创建的是引用，与原始对象指向同一内存地址")
print("2. 浅拷贝创建了新列表，但内部元素仍引用原始对象")
print("3. 不可变元素修改后：赋值对象会变化，拷贝对象不受影响")
print("4. 可变元素内部修改后：赋值对象和拷贝对象都会变化")
