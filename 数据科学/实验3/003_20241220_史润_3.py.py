import numpy as np

# 1. 创建一维数组a
a = np.array([2, 4, 6, 8, 10, 12])
print("原始数组a:", a)
# (1) a的类型
print("\n(1) a的类型:", type(a))
# (2) a的shape和size
print("\n(2) a的shape:", a.shape)
print("    a的size:", a.size)
# (3) 输出a的第5个元素
print("\n(3) a的第5个元素:", a[4])
# (4) 将a转换为2*3的矩阵，并输出新矩阵的shape和size
matrix = a.reshape(2, 3)
print("\n(4) 转换后的2*3矩阵:\n", matrix)
print("    新矩阵的shape:", matrix.shape)
print("    新矩阵的size:", matrix.size)
# (5) 从新矩阵中索引输出[10, 12]
result = matrix[1, 1:]  # 第二行的后两个元素
print("\n(5) 索引输出结果:", result)
# (6) 利用"布尔值索引"输出a中大于4的数
greater_than_4 = a[a > 4]
print("\n(6) a中大于4的数:", greater_than_4)
# (7) 重新指定数组a的数据类型为浮点数（float64），并输出其dtype
a_float = a.astype(np.float64)
print("\n(7) 转换为float64后的dtype:", a_float.dtype)
# (8) 将a中全部元素缩小10，对比around、ceil、floor的不同舍入效果
a_scaled = a_float / 10
print("\n(8) 缩小10倍后的数组:", a_scaled)
print("    around舍入结果:", np.around(a_scaled))
print("    ceil舍入结果:", np.ceil(a_scaled))
print("    floor舍入结果:", np.floor(a_scaled))

# ------------2------------
import numpy as np

# (1) empty：创建指定形状和类型的未初始化数组
empty_arr = np.empty((2, 3))
print("\n(1) empty创建的2×3数组：")
print(empty_arr)

# (2) zeros：创建全为0的数组
zeros_arr = np.zeros((3, 2), dtype=int)
print("\n(2) zeros创建的3×2整数数组：")
print(zeros_arr)

# (3) ones：创建全为1的数组
ones_arr = np.ones((2, 2, 2), dtype=float)
print("\n(3) ones创建的2×2×2浮点数组：")
print(ones_arr)

# (4) full：创建填充指定值的数组
full_arr = np.full((3, 4), 7)
print("\n(4) full创建的3×4填充7的数组：")
print(full_arr)

# (5) arange：创建[1, 2, 3, 4, 5]
arr1 = np.arange(1, 6)  # 从1开始，到6结束（不包含6）
print("\n(5) arange创建的arr1：")
print(arr1)

# (6) linspace：创建[1, 3, 5, 7, 9]
# 从1到9，生成5个等间隔的数
arr2 = np.linspace(1, 9, 5, dtype=int)
print("\n(6) linspace创建的arr2：")
print(arr2)

# (7) rand：生成0-1均匀分布的3×4×2随机三维数组
# 设置随机种子，保证结果可复现
np.random.seed(42)
rand_3d = np.random.rand(3, 4, 2)
print("\n(7) rand生成的3×4×2随机三维数组：")
print(rand_3d)
print("数组形状：", rand_3d.shape)

print()
# ------------3------------
import numpy as np

# 创建两个3行3列的数组A和B
np.random.seed(42)  # 设置随机种子，确保结果可复现
A = np.random.randint(1, 10, size=(3, 3))  # 1-9的随机整数
B = np.random.randint(1, 10, size=(3, 3))  # 1-9的随机整数
print("数组A:")
print(A)
print("\n数组B:")
print(B)
# (1) 加法、减法、乘法（矩阵乘法和哈达玛积）运算
print("\n(1) 数组运算结果：")
print("A + B:")
print(A + B)
print("\nA - B:")
print(A - B)
print("\n哈达玛积 (A * B - 对应元素相乘):")
print(A * B)
print("\n矩阵乘法 (A @ B):")
print(A @ B)  # 等同于np.matmul(A, B)
# (2) 比较运算，输出A大于等于B的比较结果
print("\n(2) A >= B 的比较结果:")
print(A >= B)
# (3) 输出A中大于等于B的值的索引
print("\n(3) A中大于等于B的值的索引:")
indices = np.where(A >= B)
# 使用zip组合索引并输出
for idx in zip(indices[0], indices[1]):
    print(f"索引 {idx}: A[{idx}] = {A[idx]}, B[{idx}] = {B[idx]}")
# (4) 输出A*B的转置矩阵
print("\n(4) A*B的转置矩阵:")
product = A * B
print(product.T)  # 等同于np.transpose(product)
# (5) 输出A和B数值对应元素相除后的余数
print("\n(5) A和B对应元素相除的余数:")
print(A % B)
# (6) 输出A第二行的元素（注意：索引从0开始，第二行即索引为1）
print("\n(6) A第二行的元素:")
print(A[1])
# (7) 输出A第三行第二列的元素[2,1]
print("\n(7) A第三行第二列的元素:")
print(A[2, 1])
# (8) 删除A的第一行，并输出
print("\n(8) 删除A的第一行后:")
A_without_first_row = np.delete(A, 0, axis=0)
print(A_without_first_row)
# (9) 删除B的第一列，并输出
print("\n(9) 删除B的第一列后:")
B_without_first_col = np.delete(B, 0, axis=1)
print(B_without_first_col)
# (10) 通过np.sum函数输出对B的按列求和，以及B的按行求和
print("\n(10) B的求和结果:")
print("按列求和:", np.sum(B, axis=0))
print("按行求和:", np.sum(B, axis=1))

print()
# ------------4------------
import pandas as pd
import numpy as np

# 创建DataFrame
data = {
    "Fruits": [
        "Apple",
        "Orange",
        " Banana ",
        " Mango ",
        " Watermelon ",
        " Grapefruit ",
    ],
    "Price": [3, 2, 2.5, 3.5, 2, 3.5],
}
df = pd.DataFrame(data)

# (1) 打印DataFrame的结果
print("(1) 原始DataFrame：")
print(df)
print()

# (2) 分别使用loc和iloc抽出"Orange"一行数据
print("(2) 使用loc提取'Orange'行：")
print(df.loc[df["Fruits"] == "Orange"])
print("\n使用iloc提取'Orange'行（已知索引为1）：")
print(df.iloc[1])
print()

# (3) 提取含有字符串 " Banana "的行，并输出返回值的数据类型
banana_row = df[df["Fruits"] == " Banana "]
print("(3) 含有' Banana '的行：")
print(banana_row)
print("返回值的数据类型：", type(banana_row))
print()

# (4) 提取出Price最贵的水果所在的行
max_price_row = df[df["Price"] == df["Price"].max()]
print("(4) 价格最贵的水果行：")
print(max_price_row)
print()

# (5) 提取出价格为3元的水果名称
price_3_fruits = df[df["Price"] == 3]["Fruits"]
print("(5) 价格为3元的水果名称：")
print(price_3_fruits.tolist())
print()

# (6) 添加一行数据['Peach', 5]（使用pandas.concat）
new_row = pd.DataFrame({"Fruits": ["Peach"], "Price": [5]})
df = pd.concat([df, new_row], ignore_index=True)
print("(6) 添加Peach后的DataFrame：")
print(df)
print()

# (7) 添加一列数据“销量”，值自拟
df["销量"] = [10, 15, 8, 12, 20, 5, 7]
print("(7) 添加销量列后的DataFrame：")
print(df)
print()

# (8) 添加一列数据“总金额”，其值通过代码计算获得（价格×销量）
df["总金额"] = df["Price"] * df["销量"]
print("(8) 添加总金额列后的DataFrame：")
print(df)
print()

# (9) 将表单按照总金额从高到低重新排序
df_sorted = df.sort_values(by="总金额", ascending=False)
print("(9) 按总金额从高到低排序：")
print(df_sorted)
print()

# (10) 分别使用loc和iloc抽出Peach和Banana行的数据
# 先找到对应索引
peach_index = df_sorted[df_sorted["Fruits"] == "Peach"].index[0]
banana_index = df_sorted[df_sorted["Fruits"] == " Banana "].index[0]

print("(10) 使用loc提取Peach和Banana行：")
print(df_sorted.loc[[peach_index, banana_index]])

# 重置索引以便使用iloc
df_sorted_reset = df_sorted.reset_index(drop=True)
peach_pos = df_sorted_reset[df_sorted_reset["Fruits"] == "Peach"].index[0]
banana_pos = df_sorted_reset[df_sorted_reset["Fruits"] == " Banana "].index[0]

print("\n使用iloc提取Peach和Banana行：")
print(df_sorted_reset.iloc[[peach_pos, banana_pos]])
print()

# (11) 提取并输出总金额高于所有总金额中位数的水果的单价
median_total = df["总金额"].median()
high_value_prices = df[df["总金额"] > median_total]["Price"]
print("(11) 总金额高于中位数的水果单价：")
print(high_value_prices.tolist())
print()

# (12) 将表单中的列标题全部改为中文
df = df.rename(columns={"Fruits": "水果", "Price": "价格"})
print("(12) 列标题改为中文后的DataFrame：")
print(df)
print()

# (13) 将DataFrame输出为"Fruits price.csv"文件
df.to_csv("Fruits price.csv", index=False, encoding="utf-8-sig")
print("(13) 'Fruits price.csv'文件已保存到当前目录")
print()

# (14) 读取"Fruits price.xlsx"文件并输出前5行数据
# 注意：需要安装openpyxl库才能读取xlsx文件 (pip install openpyxl)
try:
    df_excel = pd.read_excel("Fruits price.xlsx")
    print("(14) 读取的Excel文件前5行数据：")
    print(df_excel.head(5))
except FileNotFoundError:
    print("(14) 请先在Excel中将csv文件另存为xlsx文件后再运行此部分")
except ImportError:
    print("(14) 请先安装openpyxl库 (pip install openpyxl) 以读取xlsx文件")
