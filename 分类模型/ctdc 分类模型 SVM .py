import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# 加载Excel文件
file_path = r'D:\bishedate\changgancdhit+阴性样本 ctdc.xlsx'
data = pd.read_excel(file_path)

# 查看数据前几行
print(data.head())

# 删除非数值型列，例如 SampleName 和 label（假设 label 是目标列）
X = data.drop(['SampleName', 'label'], axis=1)  # 假设 'SampleName' 和 'label' 是非数值列
y = data['label']  # 目标变量

# 确保只包含数值型数据（如果有其他非数值列，需要进一步处理）
X = X.apply(pd.to_numeric, errors='coerce')  # 强制转换为数值型，无法转换的将变为 NaN

# 处理缺失值（如果存在的话）
X = X.fillna(X.mean())  # 使用列的均值填充缺失值

# 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# SVM 超参数调优：网格搜索
param_grid = {
    'C': [0.1, 1, 10, 100],  # 惩罚参数 C
    'gamma': ['scale', 'auto', 0.1, 1],  # 核函数参数 gamma
    'kernel': ['linear', 'rbf', 'poly']  # 核函数类型
}

# 使用网格搜索和交叉验证
grid_search = GridSearchCV(SVC(), param_grid, cv=5, scoring='accuracy', n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)

# 输出最优参数
print("Best parameters found: ", grid_search.best_params_)

# 使用最优参数训练模型
best_svm_model = grid_search.best_estimator_

# 预测并评估模型
y_pred = best_svm_model.predict(X_test)
print(classification_report(y_test, y_pred))

# 可视化混淆矩阵
cm = confusion_matrix(y_test, y_pred)

# 创建热力图进行可视化
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Non-Antibiotic', 'Antibiotic'], yticklabels=['Non-Antibiotic', 'Antibiotic'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()
