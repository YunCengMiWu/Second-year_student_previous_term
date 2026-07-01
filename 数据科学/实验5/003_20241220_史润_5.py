import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.datasets import load_iris

# ① 加载并初步查看 Iris 数据集
# 加载Iris数据集
iris = load_iris()

# 打印iris.data的前5行
print("iris.data的前5行：")
print(iris.data[:5])
print()

# 打印iris.target的后5行
print("iris.target的后5行：")
print(iris.target[-5:])
print()

# 打印iris.feature_names
print("iris.feature_names：")
print(iris.feature_names)
print()

# 打印数据描述的前300个字符
print("iris.DESCR的前300个字符：")
print(iris.DESCR[:300])

# ② 创建一个包含特征和标签的 pandas DataFrame
print("② 创建一个包含特征和标签的 pandas DataFrame")
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df["target"] = iris.target  # 新增'target'列存储标签
column_mapping = {
    "sepal length (cm)": "花萼长度",
    "sepal width (cm)": "花萼宽度",
    "petal length (cm)": "花瓣长度",
    "petal width (cm)": "花瓣宽度",
}  # 重命名特征列为中文
df.rename(columns=column_mapping, inplace=True)
# 打印前5行验证
print("DataFrame前5行：")
print(df.head())
print()

# ③ 特征量的分布分析
print("③ 特征量的分布分析")
print()
# 设置中文显示
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False
sepal_width = df["花萼宽度"]  # 直接使用中文列名提取数据

plt.figure(figsize=(12, 5))
# 分位数图
plt.subplot(1, 2, 1)
sorted_data = sepal_width.sort_values()
n = len(sorted_data)
quantiles = [(i + 1) / (n + 1) for i in range(n)]  # 计算分位值
plt.scatter(quantiles, sorted_data, color="green", alpha=0.6)
plt.xlabel("分位值（0~1）")
plt.ylabel("花萼宽度（cm）")
plt.title("花萼宽度的分位数图")
plt.grid(linestyle="--", alpha=0.5)
# Q-Q图
plt.subplot(1, 2, 2)
stats.probplot(sepal_width, dist="norm", plot=plt)
plt.title("花萼宽度的Q-Q图（评估正态性）")
plt.grid(linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()
print()
# ④ 编写基于 3σ 原则的异常值检测函数，应用于“花萼宽度”列
print("④ 编写基于 3σ 原则的异常值检测函数，应用于“花萼宽度”列")
print()


def detect_3sigma(series):  # 定义3σ异常值检测函数
    """
    基于3σ原则检测异常值
    参数：series - 待检测的pandas Series
    返回：异常值的Series（包含索引和值）
    """
    mean = series.mean()  # 均值
    std = series.std()  # 标准差
    upper_limit = mean + 3 * std  # 上限
    lower_limit = mean - 3 * std  # 下限
    outliers = series[
        (series > upper_limit) | (series < lower_limit)
    ]  # 筛选出超过上下限的值（异常值）
    return outliers


sepal_width = df["花萼宽度"]
outliers_3sigma = detect_3sigma(sepal_width)  # 2. 应用函数检测“花萼宽度”列的异常值

# 打印异常值结果
print(f"异常值数量：{len(outliers_3sigma)}")
if len(outliers_3sigma) > 0:
    print("异常值具体数值（索引: 值）：", outliers_3sigma)
    # print(outliers_3sigma)
else:
    print("未检测到异常值")
print()

# 绘制“花萼宽度”的直方图与核密度估计曲线
plt.figure(figsize=(10, 6))
sepal_width.plot(
    kind="hist", bins=15, density=True, alpha=0.6, color="lightblue", label="直方图"
)  # 直方图（density=True使纵轴为密度，与核密度曲线匹配）
sepal_width.plot(
    kind="kde", color="red", linewidth=2, label="核密度估计"
)  # 核密度估计曲线
# 添加3σ上下限参考线
mean = sepal_width.mean()
std = sepal_width.std()
plt.axvline(mean + 3 * std, color="green", linestyle="--", label="3σ上限")
plt.axvline(mean - 3 * std, color="green", linestyle="--", label="3σ下限")

plt.xlabel("花萼宽度（cm）")  # 添加标签和标题
plt.ylabel("密度")
plt.title("花萼宽度的直方图与核密度估计曲线")
plt.legend()
plt.grid(linestyle="--", alpha=0.5)
plt.show()
print()

# ⑤ 使用 IQR 方法（箱线图准则）检测“花萼宽度”中的异常值
print("⑤ 使用 IQR 方法（箱线图准则）检测“花萼宽度”中的异常值")
print()

Q1 = df["花萼宽度"].quantile(0.25)  # 下四分位数（25%分位数）
Q3 = df["花萼宽度"].quantile(0.75)  # 上四分位数（75%分位数）
IQR = Q3 - Q1  # 四分位距
lower_bound = Q1 - IQR * 1.5  # 异常值下限
upper_bound = Q3 + IQR * 1.5  # 异常值上限
wrongdatabox = df[
    (df["花萼宽度"] < lower_bound) | (df["花萼宽度"] > upper_bound)
]  # 筛选异常值数据（包含所有特征和标签，便于完整查看异常样本）
print(f"下四分位数（Q1）：{Q1:.2f}")
print(f"上四分位数（Q3）：{Q3:.2f}")
print(f"四分位距（IQR）：{IQR:.2f}")
print(f"异常值判定范围：小于{lower_bound:.2f} 或 大于{upper_bound:.2f}")
print(f"检测到的异常值数量：{len(wrongdatabox)}")
print("\n异常数据（包含所有特征和标签）：")
print(wrongdatabox)  # 打印结果

plt.figure(figsize=(8, 6))  # 绘制箱线图可视化异常值
plt.boxplot(
    df["花萼宽度"],
    patch_artist=True,
    boxprops=dict(facecolor="lightblue", color="blue"),
    flierprops=dict(marker="o", color="red", markersize=8),  # 突出显示异常值
    medianprops=dict(color="green", linewidth=2),
)
plt.xticks([1], ["花萼宽度（cm）"])
plt.ylabel("数值")
plt.title("花萼宽度的箱线图（异常值标记）")

plt.axhline(
    lower_bound, color="orange", linestyle="--", label=f"下限: {lower_bound:.2f}"
)  # 添加下限参考线
plt.axhline(
    upper_bound, color="orange", linestyle="--", label=f"上限: {upper_bound:.2f}"
)  # 添加上限参考线
plt.legend()
plt.grid(linestyle="--", alpha=0.5, axis="y")
plt.show()  # 绘图
# ------------------------   2   ---------------------------------#
# ------------------------------------------------------------------------------#
import scipy.stats as stats

# ① 输出零假设与备择假设
print("=== 卡方拟合优度检验假设 ===")
print(
    f"零假设 H0：2025年该公司110kV及以上变压器的各类故障原因分布比例与历史分布一致，即："
)
print(
    f"          绝缘老化占40%、过载运行占30%、制造缺陷占20%、外部短路占10%，无系统性偏移。"
)
print(
    f"备择假设 H1：2025年该公司110kV及以上变压器的故障原因分布比例与历史分布不一致，存在系统性偏移。"
)
print("===========================\n")

# ② 期望频数
observed = [
    92,
    58,
    32,
    18,
]  # 2025年实际故障次数：绝缘老化、过载运行、制造缺陷、外部短路
expected = [80, 60, 40, 20]  # 基于历史比例的期望频数（总故障数200）
print(f"期望频数：{expected}\n")
# ③ 计算卡方统计量
chi2_stat = sum(((o - e) ** 2) / e for o, e in zip(observed, expected))
print(f"卡方统计量：{chi2_stat:.4f}\n")

# 确定自由度（类别数-1）
df = len(observed) - 1  # 4类故障，自由度=3

# ④ 临界值（α=0.05） p值 α=0.05下统计决策
critical_value = stats.chi2.ppf(1 - 0.05, df)
p_value = stats.chi2.sf(chi2_stat, df)
print(f"自由度：{df}\n")
print(f"α=0.05时的临界值：{critical_value:.4f}\n")
print(f"p值：{p_value:.4f}")
if chi2_stat > critical_value or p_value < 0.05:
    print("\n结论：拒绝零假设（H0），2025年故障模式与历史分布存在显著差异。")
else:
    print("\n结论：不拒绝零假设（H0），2025年故障模式与历史分布无显著差异。")
# ------------------------   3   ---------------------------------#
# ------------------------------------------------------------------------------#
import pandas as pd
import scipy.stats as stats

print()
# ① 输出假设与备择假设
print("=== 卡方独立性检验假设 ===")
print(
    f"零假设 H0：断路器是否发生非计划停运与其所采用的运维策略相互独立（无统计关联）。"
)
print(
    f"备择假设 H1：断路器是否发生非计划停运与其所采用的运维策略不独立（存在统计关联）。"
)
print("===========================\n")

# ②  构建列联表
data = {"发生非计划停运": [45, 20], "未发生非计划停运": [105, 130]}
contingency_table = pd.DataFrame(data, index=["传统定期检修", "预测性维护"])
print("=== 列联表 ===")
print(contingency_table, "\n")

# ③ 计算期望频数矩阵与卡方统计量
row_totals = contingency_table.sum(axis=1)  # 每行总样本数
col_totals = contingency_table.sum(axis=0)  # 每列总样本数
total = contingency_table.sum().sum()  # 总样本数

expected = []  # 构建期望频数矩阵
for i in range(len(row_totals)):
    row = []
    row_total = row_totals.iloc[i]  # 用iloc按位置访问，避免索引警告
    for j in range(len(col_totals)):
        col_total = col_totals.iloc[j]
        exp_val = (row_total * col_total) / total
        row.append(exp_val)
    expected.append(row)  # 将每行数据添加到列表
expected_df = pd.DataFrame(
    expected, index=contingency_table.index, columns=contingency_table.columns
)  # 转换为DataFrame
print("=== 期望频数矩阵 ===")
print(expected_df.round(2), "\n")  # 保留2位小数
chi2_stat = ((contingency_table - expected_df) ** 2 / expected_df).sum().sum()
print(f"卡方统计量：{chi2_stat:.4f}\n")  # 计算输出卡方统计量

# ④ 卡方独立性检验（α=0.05）
df = (contingency_table.shape[0] - 1) * (contingency_table.shape[1] - 1)  # 自由度
critical_value = stats.chi2.ppf(1 - 0.05, df)  # 临界值
p_value = stats.chi2.sf(chi2_stat, df)  # p值

print(f"自由度：{df}")
print(f"α=0.05时的临界值：{critical_value:.4f}")
print(f"p值：{p_value:.6f}\n")

# 统计决策
if chi2_stat > critical_value or p_value < 0.05:
    print("结论：拒绝零假设（H0），运维策略与非计划停运存在统计关联。")
    # 计算可靠率，比较未发生非计划停运的比例
    traditional_ratio = (
        contingency_table.loc["传统定期检修", "未发生非计划停运"]
        / row_totals["传统定期检修"]
    )
    predictive_ratio = (
        contingency_table.loc["预测性维护", "未发生非计划停运"]
        / row_totals["预测性维护"]
    )
    print(f"传统定期检修未发生停运比例：{traditional_ratio:.2%}")
    print(f"预测性维护未发生停运比例：{predictive_ratio:.2%}")
    print("因此，预测性维护在可靠性上更具优势。")
else:
    print("结论：不拒绝零假设（H0），即运维策略与非计划停运无统计关联。")
print()
