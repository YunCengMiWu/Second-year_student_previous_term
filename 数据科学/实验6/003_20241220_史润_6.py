import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 解决中文乱码问题（根据操作系统调整字体）
plt.rcParams["font.sans-serif"] = ["SimHei"]  # Windows系统
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示异常

# 加载数据并查看基本信息
df = pd.read_csv("transformer_full.csv")  # 加载数据集
# 打印数据基本信息
print("=" * 50)
print("数据集基本信息：")
print(f"样本数量：{df.shape[0]}, 特征数量：{df.shape[1]}")
print("\n数据类型：")
print(df.dtypes)
print("\n数据统计描述（数值型特征）：")
print(df.describe().round(2))  # 保留2位小数，快速了解数据分布
print()
# --------------------缺失值分析---------------------#
# 计算缺失值数量和占比
missing_count = df.isnull().sum()  # 每个特征的缺失值数量
missing_ratio = (missing_count / len(df)) * 100  # 缺失值占总样本的比例（%）

# 整理为DataFrame，按缺失比例降序排列
missing_df = pd.DataFrame(
    {
        "特征名称": missing_count.index,
        "缺失数量": missing_count.values,
        "缺失比例(%)": missing_ratio.round(2),
    }
).sort_values("缺失比例(%)", ascending=False)

# 输出结果
print("缺失值分析结果：")
print(missing_df[missing_df["缺失数量"] > 0])  # 只显示有缺失值的特征
if (missing_count == 0).all():
    print("所有特征均无缺失值")
print()

# --------------------异常值分析---------------------#
features_normal_range = {
    "绕组温度(℃)": (50, 85),
    "油温(℃)": (45, 80),
    "油中气体含量(ppm)": (0, 100),
    "绝缘电阻(Ω)": (1e9, float("inf")),
    "局部放电量(pC)": (0, 100),
    "振动幅度(mm/s)": (0, 5),
    "噪声水平(dB)": (50, 65),
    "负载率(%)": (0, 100),
    "温度差值(°C)": (5, 15),
    "局部放电_标准分": (-3, 3),
}


# ----------------------------异常值识别与统计-----------------------------------
def detect_outliers(feature_series, feature_name):
    data = feature_series.dropna()
    if data.empty:
        return pd.Series(dtype="float64")

    if feature_name in features_normal_range:  # 基于元数据的物理范围异常
        low, high = features_normal_range[feature_name]
        phys_outliers = data[(data < low) | (data > high)]
    else:
        phys_outliers = pd.Series()  # 无元数据时，跳过物理范围过滤

    remaining_data = data.drop(phys_outliers.index) if not phys_outliers.empty else data
    if len(remaining_data) < 4:
        iqr_outliers = pd.Series()  # 数据量过少，无法计算IQR
    else:
        Q1 = remaining_data.quantile(0.25)
        Q3 = remaining_data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        iqr_outliers = remaining_data[
            (remaining_data < lower_bound) | (remaining_data > upper_bound)
        ]

    pieces = [s for s in (phys_outliers, iqr_outliers) if not s.empty]
    return (
        pd.concat(pieces).drop_duplicates() if pieces else pd.Series()
    )  # 合并异常值（去重）


outlier_stats = {}  # 统计每个特征的异常值
for feature in df.columns:
    outliers = detect_outliers(df[feature], feature)
    valid = len(df[feature].dropna())
    outlier_stats[feature] = {
        "异常值数量": len(outliers),
        "异常值占有效样本比例(%)": (
            round(len(outliers) / valid * 100, 2) if valid else 0.0
        ),
    }

outlier_df = pd.DataFrame(outlier_stats).T.sort_values("异常值数量", ascending=False)
print("异常值分析结果（结合属性的物理意义和IQR方法）：")
print(outlier_df[outlier_df["异常值数量"] > 0])  # 只显示有异常值的特征
if (outlier_df["异常值数量"] == 0).all():
    print("所有特征均无异常值")
print()
# ----------------属性冗余分析-----------------#
cov_matrix = df.cov().round(2)  # 计算协方差矩阵
corr_matrix = df.corr(method="pearson").round(3)  # 计算Pearson相关系数矩阵
# 输出协方差矩阵
print("协方差矩阵：")
print(cov_matrix)
print()
plt.figure(figsize=(12, 10))  # 绘制相关系数矩阵热力图
sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".3f",
    linewidths=0.5,
    vmin=-1,
    vmax=1,
    cbar_kws={"label": "Pearson相关系数"},
)  # 绘制热力图，annot=True显示相关系数数值，cmap='coolwarm'区分正负相关
plt.title("特征相关系数矩阵热力图", fontsize=16, pad=20)
plt.tight_layout()
plt.savefig("correlation_heatmap.png", dpi=300, bbox_inches="tight")  # 保存图片
plt.show()

high_corr_pairs = []  # 识别高相关特征对（|r|>0.8）
features = corr_matrix.columns
# 遍历上三角矩阵（避免重复配对，如(A,B)和(B,A)）
for i in range(len(features)):
    for j in range(i + 1, len(features)):
        corr_val = corr_matrix.iloc[i, j]
        if abs(corr_val) > 0.8:
            high_corr_pairs.append(
                {
                    "特征1": features[i],
                    "特征2": features[j],
                    "相关系数": corr_val,
                    "相关类型": "正相关" if corr_val > 0 else "负相关",
                }
            )
print("高相关特征对（|r|>0.8）：")  # 输出高相关特征对
if high_corr_pairs:
    high_corr_df = pd.DataFrame(high_corr_pairs)
    print(high_corr_df)
else:
    print("无高相关特征对")
print()
# ================= 2. 数据清洗 =================
print("2.数据清洗")
# 2-1 元组冗余处理：删除完全重复行
dup_cnt = df.duplicated().sum()
df = df.drop_duplicates()
print(f"删除完全重复行：{dup_cnt} 条")
print()
# 2-2 缺失值处理
# 策略说明：
#   - 数值型特征：用中位数填充，避免均值受极端值影响
#   - 类别型特征：用众数填充，保证出现频率最高的类别
num_cols = df.select_dtypes(include=np.number).columns
cat_cols = df.select_dtypes(exclude=np.number).columns
for col in num_cols:
    if df[col].isnull().any():
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
        print(f"【{col}】缺失值用中位数 {median_val} 填充")
print()
for col in cat_cols:
    if df[col].isnull().any():
        mode_val = df[col].mode()[0]
        df[col] = df[col].fillna(mode_val)
        print(f"【{col}】缺失值用众数 '{mode_val}' 填充")
print()
# 2-3 异常值处理
# 策略说明：
#   - 将 detect_outliers 识别出的异常值用该特征的中位数替换
#   - 既保留样本其余信息，又消除极端影响
outlier_cnt = 0
for col in df.columns:
    outliers = detect_outliers(df[col], col)
    if not outliers.empty:
        median_val = df[col].median()
        df.loc[outliers.index, col] = median_val
        outlier_cnt += len(outliers)
        print(f"【{col}】{len(outliers)} 个异常值已替换为中位数 {median_val}")
print(f"异常值处理完成，共处理 {outlier_cnt} 个异常样本")
print("数据清洗结束！")
print()

# ================= 3. 数据采样（简单随机抽样对比） =================
print("3. 数据采样（简单随机抽样对比）")
target_col = "绕组温度"
if target_col not in df.columns:
    print("未找到字段 '{}'，请检查列名！".format(target_col))
else:
    n_sample = 100  # 每次抽 100 条
    n_repeat = 100  # 重复 100 次
    mean_replace = []  # 有放回均值列表
    mean_no_replace = []  # 无放回均值列表

    for _ in range(n_repeat):
        # 有放回
        sample_r = df[target_col].sample(n=n_sample, replace=True)
        mean_replace.append(sample_r.mean())

        # 无放回
        sample_nr = df[target_col].sample(n=n_sample, replace=False)
        mean_no_replace.append(sample_nr.mean())

    # 画直方图
    plt.figure(figsize=(10, 6))
    plt.hist(
        mean_replace, bins=20, alpha=0.6, label="有放回 (replace=True)", color="skyblue"
    )
    plt.hist(
        mean_no_replace,
        bins=20,
        alpha=0.6,
        label="无放回 (replace=False)",
        color="salmon",
    )
    plt.axvline(df[target_col].mean(), color="red", linestyle="--", label="总体均值")
    plt.xlabel("绕组温度均值")
    plt.ylabel("频次")
    plt.title(f"{n_repeat} 次抽样均值的分布对比（每次 n={n_sample}）")
    plt.legend()
    plt.tight_layout()
    plt.savefig("sampling_compare.png", dpi=300)
    plt.show()

    var_r = np.var(mean_replace, ddof=1)
    var_nr = np.var(mean_no_replace, ddof=1)
    print(f"有放回   均值分布方差：{var_r:.6f}")
    print(f"无放回   均值分布方差：{var_nr:.6f}")
    print(f"方差减少率：{(var_r - var_nr) / var_r * 100:.2f}%")
print()

# ================= 4. 特征离散化方法 =================
print("4. 特征离散化方法")
discrete_col = "负载率(%)"
if discrete_col not in df.columns:
    # 如果列名没有括号，再试一次
    discrete_col = "负载率"
if discrete_col not in df.columns:
    print("未找到字段 '{}'，请检查列名！".format(discrete_col))
else:
    # 1) 负载率离散化
    # ---- 等宽离散化 ----
    width_labels = ["低负载", "中负载", "高负载"]
    df["等宽离散"] = pd.cut(df[discrete_col], bins=3, labels=width_labels)

    # ---- 等频离散化 ----
    freq_labels = ["低频", "中频", "高频"]
    df["等频离散"] = pd.qcut(df[discrete_col], q=3, labels=freq_labels)

    # ---- 业务规则离散化 ----
    def business_rule(x):
        if x < 40:
            return "低负载"
        elif x < 70:
            return "中负载"
        else:
            return "高负载"

    df["业务规则离散"] = df[discrete_col].map(business_rule)

    # 2) 统计各类别样本数
    count_width = df["等宽离散"].value_counts().sort_index()
    count_freq = df["等频离散"].value_counts().sort_index()
    count_biz = df["业务规则离散"].value_counts().sort_index()

    print("等宽离散化样本分布：")
    print(count_width)
    print("\n等频离散化样本分布：")
    print(count_freq)
    print("\n业务规则离散化样本分布：")
    print(count_biz)

    # 3) 可视化对比
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    count_width.plot(kind="bar", ax=axes[0], color="skyblue", title="等宽离散")
    count_freq.plot(kind="bar", ax=axes[1], color="orange", title="等频离散")
    count_biz.plot(kind="bar", ax=axes[2], color="green", title="业务规则离散")
    for ax in axes:
        ax.set_ylabel("样本数")
        ax.set_xlabel("类别")
        ax.tick_params(axis="x", rotation=0)
    plt.tight_layout()
    plt.savefig("discrete_compare.png", dpi=300)
    plt.show()

    # 4) 简单业务讨论
    print("\n=== 业务差异讨论 ===")
    print(
        "1. 等宽离散：区间等宽，但样本数可能极不均衡；"
        "当数据分布偏斜时，高负载段样本极少，不利于建模。"
    )
    print(
        "2. 等频离散：每段样本数相等，统计稳定性好，"
        "但可能把相近负载值分到不同段，业务解释性弱。"
    )
    print(
        "3. 业务规则离散：按实际运行经验划分，解释性最强，"
        "且能与运维手册直接对应；缺点是需人工设定阈值。"
    )
print()

# ================= 5. 标准化处理方法 =================
print("5. 标准化处理方法")
print()


def min_max_scale(series):  # min-max 归一化函数封装
    """Min-Max 归一化 -> [0, 1]"""
    return (series - series.min()) / (series.max() - series.min())


def z_score_scale(series):  # Z-score 标准化函数封装
    """Z-score 标准化 -> 均值 0，方差 1"""
    return (series - series.mean()) / series.std()


def decimal_scaling(series):  # 小数定标的标准化函数封装
    """小数定标标准化 -> 除以 10^k，使绝对值最大 < 1"""
    k = int(np.ceil(np.log10(series.abs().max())))
    return series / (10**k)


# 对数值型字段做演示（取前 5 列示意）
demo_cols = df.select_dtypes(include=np.number).columns[:5]
scaled_df = df[demo_cols].copy()
for col in demo_cols:
    scaled_df[f"{col}_minmax"] = min_max_scale(df[col])
    scaled_df[f"{col}_zscore"] = z_score_scale(df[col])
    scaled_df[f"{col}_decimal"] = decimal_scaling(df[col])
# 打印前 5 行对比
print("原始值 vs 三种标准化（前 5 行示例）：")
print(scaled_df.head())
print()
# 保存完整结果
scaled_df.to_csv("standardized_demo.csv", index=False, float_format="%.6f")
print("\n已保存 standardized_demo.csv，包含所有标准化结果。")
print()

# ================= 6. PCA 降维与可视化 =================
print("6. PCA 降维与可视化")

from sklearn.decomposition import PCA

# 1) 量纲问题诊断
num_df = df.select_dtypes(include=np.number)
var_series = num_df.var().sort_values(ascending=False)
print("清洗后数据各特征方差（降序）：")
print(var_series.round(2))
max_var_feat = var_series.index[0]
print()
print(f"量纲差异最大特征：{max_var_feat}（方差={var_series.iloc[0]:.2f}）")
print()

# 2) 对比 PCA 效果
pca_2d = PCA(n_components=2, random_state=42)

# ---- 未标准化直接 PCA ----
X_raw = num_df.values
pca_raw = pca_2d.fit_transform(X_raw)
# ---- 清洗后的数据在Z-score标准化后 PCA  ----
X_std = num_df.apply(z_score_scale).values
pca_std = pca_2d.fit_transform(X_std)

# 绘制 2D 散点图对比
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].scatter(pca_raw[:, 0], pca_raw[:, 1], alpha=0.6, s=15)
axes[0].set_title("未标准化直接 PCA")
axes[0].set_xlabel("PC1")
axes[0].set_ylabel("PC2")

axes[1].scatter(pca_std[:, 0], pca_std[:, 1], alpha=0.6, s=15, color="orange")
axes[1].set_title("Z-score 标准化后 PCA")
axes[1].set_xlabel("PC1")
axes[1].set_ylabel("PC2")
plt.tight_layout()
plt.savefig("pca_2d_compare.png", dpi=300)
plt.show()

# 3) 标准化后 PC1 权重分析
pca_std_fit = PCA(n_components=2, random_state=42).fit(X_std)
pc1_loadings = pca_std_fit.components_[0]  # 第一主成分权重
loadings_abs = np.abs(pc1_loadings)
loadings_df = pd.DataFrame(
    {"特征": num_df.columns, "PC1_权重绝对值": loadings_abs}
).sort_values("PC1_权重绝对值", ascending=True)

# 水平条形图
plt.figure(figsize=(6, 8))
plt.barh(loadings_df["特征"], loadings_df["PC1_权重绝对值"], color="steelblue")
plt.xlabel("PC1 权重绝对值")
plt.title("第一主成分（PC1）各特征贡献度")
plt.tight_layout()
plt.savefig("pca_pc1_weights.png", dpi=300)
plt.show()

print("对 PC1 贡献最大的前 3 个特征：")
print(loadings_df.tail(3).iloc[::-1])
