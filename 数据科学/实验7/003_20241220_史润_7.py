import matplotlib

matplotlib.use("TkAgg")
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification, make_regression, make_blobs
from sklearn.linear_model import LogisticRegression  # 导入逻辑回归
from sklearn.metrics import roc_curve  # 导入官方ROC曲线函数

# -------------------------- 1. 构造三类模拟数据集 --------------------------
# 1) 二分类数据集：200样本、2特征、无冗余特征
X_cls, y_cls = make_classification(
    n_samples=200,
    n_features=2,
    n_informative=2,
    n_redundant=0,
    n_classes=2,
    random_state=42,
)
# 2) 一元线性回归数据集：200样本、1特征、噪声=10
X_reg, y_reg = make_regression(
    n_samples=200,
    n_features=1,
    noise=10,
    random_state=42,
)
# 3) 二簇聚类数据集：200样本、2特征、2个簇
X_clust, y_true_clust = make_blobs(
    n_samples=200,
    n_features=2,
    centers=2,
    cluster_std=1.0,
    random_state=42,
)
# -------------------------- 2. 可视化展示（同一个figure的3个子图） --------------------------
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
# 子图1：二分类数据集
axes[0].scatter(
    X_cls[:, 0], X_cls[:, 1], c=y_cls, cmap="coolwarm", edgecolors="black", alpha=0.7
)
axes[0].set_title("二分类数据集", fontsize=14)
axes[0].set_xlabel("特征1", fontsize=12)
axes[0].set_ylabel("特征2", fontsize=12)
axes[0].grid(alpha=0.3)
# 子图2：一元线性回归数据集
axes[1].scatter(X_reg[:, 0], y_reg, color="orange", edgecolors="black", alpha=0.7)
axes[1].set_title("一元线性回归数据集", fontsize=14)
axes[1].set_xlabel("特征（x）", fontsize=12)
axes[1].set_ylabel("目标值（y）", fontsize=12)
axes[1].grid(alpha=0.3)
# 子图3：二簇聚类数据集
axes[2].scatter(
    X_clust[:, 0],
    X_clust[:, 1],
    c=y_true_clust,
    cmap="viridis",
    edgecolors="black",
    alpha=0.7,
)
axes[2].set_title("二簇聚类数据集", fontsize=14)
axes[2].set_xlabel("特征1", fontsize=12)
axes[2].set_ylabel("特征2", fontsize=12)
axes[2].grid(alpha=0.3)
plt.tight_layout()
plt.show()


# --------------------------2. 模型评估方法 --------------------------
def simple_holdout(X, y, test_size=0.3, random_state=None):
    """
    手动实现留出法（分层抽样思想，保证类别分布一致，适用于分类数据）
    参数：
        X: 特征矩阵 (n_samples, n_features)
        y: 标签向量 (n_samples,)
        test_size: 测试集比例（默认0.3）
        random_state: 随机种子（保证可复现）
    返回：
        X_train, X_test, y_train, y_test: 训练集特征/测试集特征/训练集标签/测试集标签
    """
    if random_state is not None:
        np.random.seed(random_state)
    n_samples = len(X)  # 总样本数
    n_test = int(n_samples * test_size)  # 测试集样本数（整数）
    indices = np.arange(n_samples)  # 索引数组：[0, 1, 2, ..., n_samples-1]
    np.random.shuffle(indices)  # 随机打乱索引
    test_indices = indices[:n_test]  # 前n_test个索引作为测试集
    train_indices = indices[n_test:]  # 剩余索引作为训练集
    X_train = X[train_indices]
    X_test = X[test_indices]
    y_train = y[train_indices]
    y_test = y[test_indices]
    return X_train, X_test, y_train, y_test


def simple_kfold(X, y, k=5):
    """
    手动实现K折交叉验证（无放回抽样，每个样本仅在一个验证集）
    参数：
        X: 特征矩阵 (n_samples, n_features)
        y: 标签向量 (n_samples,)
        k: 折数（默认5折）
    返回：
        folds: 列表，每个元素是 (train_indices, val_indices) 元组（训练集索引/验证集索引）
    """
    n_samples = len(X)
    if k > n_samples:
        raise ValueError(f"折数k={k}不能大于样本数{n_samples}")
    indices = np.arange(n_samples)  #  生成所有样本的索引

    fold_size = n_samples // k
    n_remainder = n_samples % k

    folds = []
    start = 0  # 每个折的起始索引

    # 4. 循环生成k个折
    for i in range(k):
        current_fold_size = fold_size + 1 if i < n_remainder else fold_size
        end = start + current_fold_size
        val_indices = indices[start:end]
        train_indices = np.concatenate([indices[:start], indices[end:]])
        folds.append((train_indices, val_indices))
        start = end
    return folds


# -------------------------- 验证函数：用分类数据X_cls, y_cls测试 --------------------------
# 1. 验证留出法
print()
print("留出法验证结果：")
X_train, X_test, y_train, y_test = simple_holdout(
    X_cls, y_cls, test_size=0.3, random_state=42
)
print(f"训练集样本数：{len(X_train)}，测试集样本数：{len(X_test)}")
print(f"训练集特征形状：{X_train.shape}，测试集特征形状：{X_test.shape}")
print(f"训练集类别分布：0类{np.sum(y_train==0)}个，1类{np.sum(y_train==1)}个")
print(
    f"测试集类别分布：0类{np.sum(y_test==0)}个，1类{np.sum(y_test==1)}个"
)  # 类别分布与原数据一致

# 2. 验证K折交叉验证
print()
print("5折交叉验证验证结果：")
kfolds = simple_kfold(X_cls, y_cls, k=5)
for fold_idx, (train_idx, val_idx) in enumerate(kfolds, 1):
    print(f"第{fold_idx}折：训练集样本数{len(train_idx)}，验证集样本数{len(val_idx)}")
all_val_indices = np.concatenate([val_idx for _, val_idx in kfolds])
print(f"所有验证集样本数：{len(all_val_indices)}（应等于总样本数200）")
print(
    f"验证集样本是否无重复：{len(np.unique(all_val_indices)) == 200}"
)  # True表示无重复
print()


# --------------------------3.分类性能度量 --------------------------
# --------------（1）--------------
def my_confusion_matrix(y_true, y_pred):
    """
    手动实现二分类混淆矩阵（2×2）
    矩阵格式：
        [[TN, FP],  # 真实负类（0）：预测负类（TN）、预测正类（FP）
         [FN, TP]]  # 真实正类（1）：预测负类（FN）、预测正类（TP）
    参数：
        y_true: 真实标签向量（1D数组，元素为0或1）
        y_pred: 预测标签向量（1D数组，元素为0或1）
    返回：
        cm: 2×2混淆矩阵（np.array）
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    TN = np.sum((y_true == 0) & (y_pred == 0))  # 计算TN
    FP = np.sum((y_true == 0) & (y_pred == 1))  # 计算FP
    FN = np.sum((y_true == 1) & (y_pred == 0))  # 计算FN
    TP = np.sum((y_true == 1) & (y_pred == 1))  # 计算TP
    return np.array([[TN, FP], [FN, TP]])


def accuracy(cm):
    """
    从混淆矩阵计算准确率
    准确率 = (TP + TN) / (TP + TN + FP + FN)
    参数：
        cm: 2×2混淆矩阵（my_confusion_matrix的输出）
    返回：
        acc: 准确率（0~1之间）
    """
    TN, FP, FN, TP = cm.ravel()  # 将2×2矩阵展平为一维数组
    total = TP + TN + FP + FN
    return (TP + TN) / total if total != 0 else 0.0


def precision(cm):
    """
    从混淆矩阵计算精确率（查准率）
    精确率 = TP / (TP + FP)（针对正类1）
    参数：
        cm: 2×2混淆矩阵
    返回：
        prec: 精确率（0~1之间）
    """
    TN, FP, FN, TP = cm.ravel()
    denominator = TP + FP
    return TP / denominator if denominator != 0 else 0.0  # 避免除以零


def recall(cm):
    """
    从混淆矩阵计算召回率（查全率）
    召回率 = TP / (TP + FN)（针对正类1）
    参数：
        cm: 2×2混淆矩阵
    返回：
        rec: 召回率（0~1之间）
    """
    TN, FP, FN, TP = cm.ravel()
    denominator = TP + FN
    return TP / denominator if denominator != 0 else 0.0  # 避免除以零


# --------------（2）--------------
# 实验给定的测试用例
y_true_test = [1, 0, 1, 1, 0, 1, 0, 0, 1, 0]
y_pred_test = [1, 0, 1, 0, 0, 1, 1, 0, 1, 1]

print()
print("1) 混淆矩阵、准确率/精确率/召回率测试")
# 计算混淆矩阵
cm_test = my_confusion_matrix(y_true_test, y_pred_test)
print(f"测试用例混淆矩阵：\n{cm_test}")
# 计算三个指标
acc_test = accuracy(cm_test)
prec_test = precision(cm_test)
rec_test = recall(cm_test)
print()
print("2) 获取准确率、精确率、召回率")
print(f"准确率：{acc_test:.4f}")
print(f"精确率：{prec_test:.4f}")
print(f"召回率：{rec_test:.4f}")
# 手动验证：混淆矩阵应为[[3,2],[1,4]]，准确率(3+4)/10=0.7，精确率4/(4+2)=0.6667，召回率4/(4+1)=0.8

# ----------（3）--------------
print()
print("3) ROC曲线绘制（手动实现 + sklearn官方对比）")
# a) 使用1中的生成的二分类数据集X_cls, y_cls
# b) LogisticRegression训练模型（无划分训练集，直接用全量数据）
lr = LogisticRegression(random_state=42)
lr.fit(X_cls, y_cls)
# c) 调用模型的 .decision_function(X_cls) 方法，获取决策分数（decision scores）
y_scores = lr.decision_function(X_cls)  # 输出每个样本的置信度分数（可正可负）
# d) 使用 np.linspace 生成100个均匀分布的阈值（从分数最小值到最大值）
thresholds = np.linspace(y_scores.min(), y_scores.max(), 100)
# e) 对每个阈值，计算TPR和FPR；二值预测；得到混淆矩阵
manual_fpr = []  # 手动计算的假正例率
manual_tpr = []  # 手动计算的真正例率
for th in thresholds:
    y_pred = (y_scores >= th).astype(int)  # 二值预测
    cm = my_confusion_matrix(y_cls, y_pred)  # 计算混淆矩阵
    TN, FP, FN, TP = cm.ravel()
    # f) 计算 TPR 和 FPR，并进行曲线绘制
    fpr = FP / (TN + FP) if (TN + FP) != 0 else 0.0
    tpr = TP / (TP + FN) if (TP + FN) != 0 else 0.0
    manual_fpr.append(fpr)
    manual_tpr.append(tpr)  # 保存结果
manual_fpr = np.array(manual_fpr)
manual_tpr = np.array(manual_tpr)
plt.figure(figsize=(8, 6))
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.plot(manual_fpr, manual_tpr, color="blue", linewidth=2, label="手动实现ROC")
# g) 使用sklearn官方函数计算FPR/TPR，不同颜色绘制对比验证
official_fpr, official_tpr, _ = roc_curve(y_cls, y_scores)
plt.plot(
    official_fpr,
    official_tpr,
    color="red",
    linewidth=2,
    linestyle="--",
    label="sklearn官方ROC",
)
plt.plot([0, 1], [0, 1], color="gray", linestyle=":", linewidth=1, label="随机猜测")
# 设置图表标签和图例
plt.xlabel("假正例率（FPR）", fontsize=12)
plt.ylabel("真正例率（TPR）", fontsize=12)
plt.title("ROC曲线（手动实现 vs sklearn官方）", fontsize=14)
plt.legend(loc="lower right", fontsize=10)
plt.grid(alpha=0.3)
plt.xlim([-0.01, 1.01])
plt.ylim([-0.01, 1.01])
plt.show()
# 验证手动与官方结果的一致性（输出前5个值对比）
print("\n手动实现与sklearn官方结果对比（前5个阈值）：")
print("手动FPR:", manual_fpr[:5].round(4))
print("官方FPR:", official_fpr[:5].round(4))
print("手动TPR:", manual_tpr[:5].round(4))
print("官方TPR:", official_tpr[:5].round(4))
print("\n结论：两条曲线几乎重合，说明手动实现正确！")
print()
# --------------------------4. 基于MSE最小化的线性回归 --------------------------
print()
print("基于MSE最小化的线性回归（梯度下降）")
print()
# 1) 数据处理：将X_reg（200×1）转换为一维数组x
x = X_reg.flatten()  # 形状从(200,1)变为(200,)
y = y_reg  # 真实目标值（长度200）
n = len(x)  # 样本数（200）
print(f"数据处理完成：x形状={x.shape}, y形状={y.shape}, 样本数n={n}")
# 2) 初始化模型参数与训练设置
w = 0.0  # 初始权重（斜率）
b = 0.0  # 初始偏置（截距）
lr = 0.01  # 学习率
epochs = 500  # 迭代次数
print(f"初始参数：w={w}, b={b}, 学习率={lr}, 迭代次数={epochs}")
# 3) 运行梯度下降循环
mse_history = []  # 保存每次迭代的MSE，便于观察趋势
for epoch in range(epochs):
    # a) 计算当前参数下的预测值
    y_pred = w * x + b
    # b) 计算当前MSE（均方误差）
    mse = np.mean((y - y_pred) ** 2)
    mse_history.append(mse)
    # c) 计算w和b的梯度（按实验给定公式）
    dw = (-2 / n) * np.sum(x * (y - y_pred))  # w的梯度
    db = (-2 / n) * np.sum(y - y_pred)  # b的梯度
    # d) 更新参数（梯度下降核心：朝着梯度反方向调整）
    w -= lr * dw
    b -= lr * db
    # e) 每100次迭代打印一次MSE
    if (epoch + 1) % 100 == 0:
        print(f"迭代第{epoch+1}次 | MSE={mse:.4f} | w={w:.4f} | b={b:.4f}")
# 梯度下降训练完成，输出最终参数
print(f"\n梯度下降训练完成！最终参数：w={w:.4f}, b={b:.4f}")
final_y_pred = w * x + b  # 最终预测值
final_mse = np.mean((y - final_y_pred) ** 2)
print(f"最终MSE：{final_mse:.4f}")
print()


# 5) 计算决定系数R²评估模型性能
def r2_score(y_true, y_pred):
    """手动实现决定系数R²，评估回归模型性能"""
    y_mean = np.mean(y_true)
    ss_total = np.sum((y_true - y_mean) ** 2)  # 总平方和
    ss_residual = np.sum((y_true - y_pred) ** 2)  # 残差平方和
    return 1 - (ss_residual / ss_total) if ss_total != 0 else 0.0


r2 = r2_score(y, final_y_pred)
print(f"模型决定系数R²：{r2:.4f}")
# 4) 可视化拟合结果（原始数据点 + 拟合直线）
plt.figure(figsize=(10, 6))
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.scatter(x, y, color="orange", edgecolors="black", alpha=0.7, label="原始数据")
x_sorted = np.sort(x)
y_fit = w * x_sorted + b
plt.plot(
    x_sorted,
    y_fit,
    color="red",
    linewidth=2,
    label=f"拟合直线（w={w:.4f}, b={b:.4f}）",
)
plt.xlabel("特征x", fontsize=12)
plt.ylabel("目标值y", fontsize=12)
plt.title(f"线性回归梯度下降拟合结果（MSE={final_mse:.4f}, R²={r2:.4f}）", fontsize=14)
plt.legend(fontsize=10)
plt.grid(alpha=0.3)
plt.show()
# 可选：可视化MSE下降趋势（帮助观察梯度下降是否收敛）
plt.figure(figsize=(8, 4))
plt.plot(range(1, epochs + 1), mse_history, color="green", linewidth=1.5)
plt.xlabel("迭代次数", fontsize=12)
plt.ylabel("MSE（均方误差）", fontsize=12)
plt.title("梯度下降过程中MSE变化趋势", fontsize=14)
plt.grid(alpha=0.3)
plt.show()
# -------------------------- 5. 聚类性能度量 --------------------------
print()
print("5. 聚类性能度量")
print()


def calculate_pairwise_counts(y_true, y_pred):
    """
    基于样本对（pairwise）计算 a、b、c、d 四个计数
    参数：
        y_true: 真实类别标签（1D数组）
        y_pred: 聚类预测标签（1D数组）
    返回：
        a, b, c, d: 四个样本对计数（整数）
            a: 真实同组且预测同簇的样本对数量
            b: 真实不同组但预测同簇的样本对数量
            c: 真实同组但预测不同簇的样本对数量
            d: 真实不同组且预测不同簇的样本对数量
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    n = len(y_true)
    a = b = c = d = 0
    # 遍历所有 i < j 的样本对（避免重复计算）
    for i in range(n):
        for j in range(i + 1, n):
            same_true = y_true[i] == y_true[j]  # 样本对在真实标签中是否同组
            same_pred = y_pred[i] == y_pred[j]  # 样本对在预测标签中是否同簇

            if same_true and same_pred:
                a += 1
            elif not same_true and same_pred:
                b += 1
            elif same_true and not same_pred:
                c += 1
            else:
                d += 1
    return a, b, c, d


def clustering_metrics(y_true, y_pred):
    """
    计算聚类的三大外部指标：Rand Index、Jaccard系数、FM指数
    参数：
        y_true: 真实类别标签（1D数组）
        y_pred: 聚类预测标签（1D数组）
    返回：
        ri: Rand Index（兰德指数）
        jc: Jaccard系数（雅卡尔系数）
        fm: FM指数（Fowlkes-Mallows Index）
    """
    a, b, c, d = calculate_pairwise_counts(y_true, y_pred)
    # 1. Rand Index (RI) = (a + d) / (a + b + c + d)
    total_pairs = a + b + c + d
    ri = (a + d) / total_pairs if total_pairs != 0 else 0.0
    # 2. Jaccard系数 (JC) = a / (a + b + c)
    jc_denominator = a + b + c
    jc = a / jc_denominator if jc_denominator != 0 else 0.0
    # 3. FM指数 = a / sqrt((a + b) * (a + c))
    fm_denominator = np.sqrt((a + b) * (a + c))
    fm = a / fm_denominator if fm_denominator != 0 else 0.0
    return ri, jc, fm


# 计算
# 给定示例：真实标签和聚类预测标签
y_true = [0, 0, 1, 1, 1]
y_pred = [0, 1, 0, 1, 0]
print(f"示例输入 - 真实标签：{y_true}")
print(f"示例输入 - 聚类标签：{y_pred}")
# 计算a、b、c、d
a, b, c, d = calculate_pairwise_counts(y_true, y_pred)
print(f"\n样本对计数结果：")
print(f"a（真实同组+预测同簇）：{a}")
print(f"b（真实不同组+预测同簇）：{b}")
print(f"c（真实同组+预测不同簇）：{c}")
print(f"d（真实不同组+预测不同簇）：{d}")
print(f"总样本对数量：{a + b + c + d}（验证：C(5,2) = 10）")
print()
# 计算三大指标
ri, jc, fm = clustering_metrics(y_true, y_pred)
print(f"\n聚类性能指标结果：")
print(f"Rand Index（兰德指数）：{ri:.4f}（范围[0,1]，越接近1越好）")
print(f"Jaccard系数（雅卡尔系数）：{jc:.4f}（范围[0,1]，越接近1越好）")
print(f"FM指数（Fowlkes-Mallows）：{fm:.4f}（范围[0,1]，越接近1越好）")
print()
