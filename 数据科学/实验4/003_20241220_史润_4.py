"""1. 利用 pandas 工具包将数据 1 和数据 2 中的数据载入并进行合并，查看合并
后的 dataframe 的前 5 行。
提示：
① concat 和 append 可以实现的是表间“拼接”，而 merge 和 join 则实现的是
表间“合并”，区别在于是否基于”键“来进行合并。如果只是简单地”堆砌“，
则用 concat 和 append 比较合适，而如果遇到关联表，需要根据”键“来合并，
则用 merge 和 join。
② concat 和 merge 是 pandas 的属性，所以调用的时候应该写成 pd.concat()
或者 pd.merge()；而 append 和 join 是对 DataFrame 的方法，所以调用的时候
应该写成 df.append()或者 df.join()。"""

import pandas as pd

df1 = pd.read_csv(r"C:\数据科学_Py\实验4\数据1.csv", encoding="ANSI")
df2 = pd.read_excel(r"C:\数据科学_Py\实验4\数据2.xlsx")
df = pd.concat([df1, df2])
print(df.head())
# 2. 对合并后的数据进行筛选，保留国籍为中国的女篮运动员数据。
df = df[(df["国籍"] == "中国") & (df["性别"] == "女") & (df["项目"] == "篮球")]

# 3. 对筛选后的数据进行清理：
# 3.1 首先对重复的行进行删除；（提示：注意字符串中的空格）
df = df.drop_duplicates(subset=["外文名"])  # 因为中文名会存在空格，所以用外文名去重
"""3.2 随后对异常值的替换，包括：
① 将身高列数据修正，使用平均值填充空值，统一为数字格式，保留一位
小数，并将列名从“身高”重命名为“身高/cm”；
② 体重列单位统一为“kg”，处理明显的错误数据，用平均值填充空值。
③ 最后将省份的空缺值修改为“未知”，使用“loc”的索引方法修改“陈
楠”的“省份”为“青岛”，使用“iloc”的索引方法修改“陈晓佳”的“省
份”为“江苏”。"""
cor = {
    "191cm": "191厘米",
    "1米89公分": "189厘米",
    "2.01米": "201厘米",
    "187公分": "187厘米",
    "192cm": "192厘米",
    "1.98米": "198厘米",
}
df.loc[:, "身高"] = df.loc[:, "身高"].replace(cor)
i = 0
for x in df.loc[:, "身高"]:
    if pd.isna(x):
        pass
    else:
        df.iloc[i, 4] = int(x[:-2])
    i += 1
df.loc[:, "身高"] = df.loc[:, "身高"].fillna(df.loc[:, "身高"].mean())
df.loc[:, "身高"] = df.loc[:, "身高"].map(lambda x: f"{x:.1f}")
df.rename(columns={"身高": "身高/cm"}, inplace=True)

df.loc[:, "体重"] = df.loc[:, "体重"].replace({"88千克": "88kg"})
df["体重"].replace("8kg", method="pad", inplace=True)
w = df["体重"].dropna()
w_m = w.apply(lambda x: x[:-2]).astype(int).mean()
str_w = f"{w_m:.0f}kg"
df.loc[:, "体重"] = df.loc[:, "体重"].fillna(str_w)

df.loc[:, "省份"] = df.loc[:, "省份"].fillna("未知")
df.loc[23, "省份"] = "青岛"
df.iloc[6, 7] = "江苏"
print(df)
"""4. 计算女篮运动员的身高数据的中位数、众数、标准差；找出身高在前 25%的
运动员，将姓名导出为 txt 文档；在同一个 figure 的左右两边分别绘制女篮
运动员的身高数据的箱型图和直方图。"""
df_h = df["身高/cm"].apply(lambda x: float(x))
print(df_h.median())
print(df_h.mode())
print(df_h.std(axis=0))
name = df_h >= df_h.quantile(0.75)
df[name]["中文名"].to_csv("导出.txt", index=False)
import matplotlib.pyplot as plt

figure, ax = plt.subplots(1, 2)
df_h = pd.DataFrame(df_h)
df_h.boxplot(column="身高/cm", ax=ax[0])
plt.ylabel("cm")
plt.subplot(1, 2, 1)
df_h.hist(column="身高/cm", ax=ax[1])
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.show()
"""5. 设计一个程序，统计 txt 文件中包含的行数和字数；利用程序统计上题导出
的姓名文档"""


def statistic(file):
    f = open(file, "r", encoding="utf-8")
    count1 = 0
    count2 = 0
    for line in f:
        if line != " ":
            count1 += 1
            print(line)
            for i in line:
                if i != "\n":
                    count2 += 1
    print(count1, count2)
    return count1, count2


statistic("导出.txt")
