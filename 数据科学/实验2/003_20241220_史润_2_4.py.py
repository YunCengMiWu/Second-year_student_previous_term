# 初始列表
my_list = ["Chongqing", "Uni", 1923, 2023]

my_list[1] = "University"  # 'Uni'改为'University'
my_list.insert(2, "year")  # 'University'后添加 'year'
my_list.append("CHINA")  # 列表最后添加 'CHINA'

print(my_list[-1].lower())  # 由列表输出'china'（将最后一个元素转为小写字母）
print(f"列表长度: {len(my_list)}")  # 输出列表长度

my_tuple = tuple(my_list)  # 将列表转换为元组
print(type(type(my_tuple)))  # 用type打印出元组的类型

has_chongqing = "Chongqing" in my_tuple  # 检查元组中是否有'Chongqing'
print(f"元组中是否包含'Chongqing': {has_chongqing}")
print("最终的元组:", my_tuple)  # 打印最终的元组，查看结果
