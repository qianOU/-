import numpy as np
from matplotlib import pyplot as plt
from sklearn.datasets import load_boston

X, Y = load_boston(return_X_y=True)
print('x.shape=', X.shape)

#标准化
# =============================================================================
# 使得 缩放数据具有零均值和单位方差
# Z-Score标准化
from sklearn import preprocessing
scaler = preprocessing.StandardScaler().fit(X)
scaler.mean_ #返回每一列的均值
scaler.scale_ #返回每一列的标准差
x_trans = scaler.transform(X)
scaler.transform(X).mean(axis=0)
scaler.transform(X).std(axis=0)
scaler.inverse_transform(x_trans)
# =============================================================================
#极大极小值归一化
# =============================================================================
#feature_range=(-1, 1) 可以指定数据变化的范围
min_max_scaler = preprocessing.MinMaxScaler(feature_range=(-1, 1)).fit(X) 
X_train_minmax = min_max_scaler.transform(X)
X_train_minmax
min_max_scaler.scale_ #查找最大值
min_max_scaler.min_ #最小值
min_max_scaler.inverse_transform(x_trans)
# =============================================================================
# 去除异常值的Z-score标准化
# =============================================================================
# 根据分位数范围（默认为 IQR：四分位数范围）缩放数据。
transformer = preprocessing.RobustScaler().fit(X)
x_trans = transformer.transform(X)
x_trans.inverse_transform(x_trans)
# =============================================================================
#数据白化，去除数据间的共线性 PCA white=True
from sklearn.decomposition import PCA
model = PCA(whiten=True) #等维度去除共线性
model.fit(X)
x_trans = model.transform(X) 
np.corrcoef(x_trans) #计算相关系数
# =============================================================================
#缩放1D数据
# =============================================================================
# 以上所有函数（即缩放、minmax_scale、maxabs_scale和robust_scale）都接受 1D 数组，这在某些特定情况下非常有用。
# =============================================================================


#非线性变换，正态化
#以下两种方法，对于均匀分布的数据失效
# =============================================================================
# 非参变换方法------QuantileTransformer 分位数变化（可以变化为均匀分布（默认）或则正态分布）
from sklearn.preprocessing import QuantileTransformer
quantile_transformer = preprocessing.QuantileTransformer(output_distribution='normal',
                                                random_state=0).fit(X)
x_trans = quantile_transformer.transform(x_trans)
quantile_transformer.inverse_transform(x_trans) #可逆
import scipy
scipy.stats.shapiro(x_trans[:,-3]) #假设检验
#因此，输入的中位数将成为输出的均值，以 0 为中心。



# 参数方法----PowerTransformer功率转换。不可逆变化(正态分布)
#Yeo-Johnson 变换和 Box-Cox 变换， 但是 Box-Cox 只能应用于严格的正数据。
# standardize = True(默认) 将应用零均值、单位方差规范化
pt = preprocessing.PowerTransformer(method='yeo-johnson', standardize=True).fit(X) #
x_trans = pt.transform(X)
import scipy
scipy.stats.shapiro(x_trans[:,-3]) #假设检验
# =============================================================================











# 规范化 l1, l2
# =============================================================================
#l2
X_normalized = preprocessing.normalize(X, norm='l2')#将每一个观测进行规范化为单位长度
(X_normalized**2).sum(axis=1) #l2
normalizer = preprocessing.Normalizer(norm='l2').fit(X)#fit方法无实际含义，只是提供相同的接口便于pipeline中使用
(normalizer.transform(X)**2).sum(axis=1)

#l1
X_normalized = preprocessing.normalize(X, norm='l1', axis=1)
(X_normalized).sum(axis=0) #l1
normalizer = preprocessing.Normalizer(norm='l1').fit(X) #fit方法无实际含义，只是提供相同的接口便于pipeline中使用
(normalizer.transform(X)).sum(axis=1)
# =============================================================================





# 编码与分类功能
# =============================================================================
# OrdinalEncoder（顺序编码）：此估计器将每个分类特征转换为整数的一个新特征（0 到 n_categories - 1）
genders = ['female', 'male']
locations = ['from Africa', 'from Asia', 'from Europe', 'from US']
browsers = ['uses Chrome', 'uses Firefox', 'uses IE', 'uses Safari']
X = [['male', 'from US', 'uses Safari'], ['female', 'from Europe', 'uses Firefox']]
#给categories 传入数组类型，告诉编码器应该如何按给定的顺序进行编码，不传入则默认“auto”
enc = preprocessing.OrdinalEncoder(categories=[genders, locations, browsers])

enc.fit(X)
enc.transform(X)
enc.categories_ #得到类名和排序


# 独热编码
#给categories 传入数组类型，告诉编码器应该如何按给定的顺序进行编码，不传入则默认“auto”
enc = preprocessing.OneHotEncoder(categories=[genders, locations, browsers])
enc.fit(X)
enc.transform(X).toarray()
enc.categories_ #得到类名和排序
#drop = "first" 将每一个特征的第一个类别设置为基类（也就是对其不编码）
# drop = ‘if_binary’ 只对二分类的特征进行删除第一类操作
# drop = array 自己设置集类

#==============================================================================


X, Y = load_boston(return_X_y=True)

# 离散化
# =============================================================================
#K 箱离散化 KBinsDiscretizer
est = preprocessing.KBinsDiscretizer(n_bins=10, encode='ordinal')
est.fit(X[:,5:7])
x_trans = est.transform(X[:,5:7])



#二值化 Binarizer
binarizer = preprocessing.Binarizer(threshold=2)
binarizer.fit(X) #do nothing
binarizer.transform(X)
# =============================================================================



#生成多项式特征
# =============================================================================
from sklearn.preprocessing import PolynomialFeatures
X = np.arange(6).reshape(3, 2)
# interaction_only=True 只产生交互项
poly = PolynomialFeatures(2)
poly.fit_transform(X)
poly.n_output_features_
poly.get_feature_names(['age', 'educ']) #产生多项式的每一列的名字

# =============================================================================

