# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 15:13:18 2020

@author: 28659
"""
from sklearn.datasets import load_iris
iris = load_iris()
X = iris.data
y = iris.target

# PCA 
#提取变量间的线性特性
# =============================================================================
# 普通PCA
# 需要数据一起读入内存中
#可以指定参数whiten=True来进一步删除转换后可能存在的相关信息
from sklearn.decomposition import PCA
pca = PCA(n_components=2, whiten=True).fit(X)
X_pca = pca.transform(X)
pca.explained_variance_ratio_
pca.components_ #返回两个主成分的方向

#增量PCA IncrementalPCA
# 处理大型数据时，数据无法一次性读入内存的问题
from sklearn.decomposition import IncrementalPCA
ipca = IncrementalPCA(n_components=2, whiten=True, batch_size=10)
ipca.fit(X)
ipca.transform(X)
ipca.explained_variance_ratio_


# 随机SVD PCA
# 数据特征十分巨大，比如图像数据，可以利用随机SVD进行降维，加快效率
spca = PCA(n_components=2, whiten=True, svd_solver='randomized').fit(X)
spca.transform(X)
spca.explained_variance_ratio_
spca.inverse_transform


#核PCA KernelPCA
#KernelPCA是PCA的扩展，它通过使用内核实现非线性维维降低
# 内核 PCA 能够找到使数据线性可分离的数据投影
from sklearn.decomposition import KernelPCA

kpca = KernelPCA(n_components=2, kernel='rbf', fit_inverse_transform=True, gamma=10)
X_kpca = kpca.fit_transform(X)
X_back = kpca.inverse_transform(X_kpca)


#SparsePCA 稀疏化PCA
# PCA的缺点是当它们表示为原始变量的线性组合时，它们具有非零系数。这会使解释变得困难
#通过对右奇异矩阵施行l1正则
from sklearn.decomposition import SparsePCA
sppca = SparsePCA(n_components=3, ridge_alpha=0.01, random_state=0)
sppca.fit(X)
sppca.transform(X)
sppca.components_  #可以看主成分包含哪些原始变量，增加了可解释性
# =============================================================================






#截断SVD TruncatedSVD
# =============================================================================
# 截断SVD，仅计算最大的k个奇异值
#截断SVD与PCA非常相似，但不同的是矩阵不需要居中。当从要素值中减去列（每个要素）的均值时，结果矩阵上的截断 SVD 等效于 PCA。实际上，这意味着截断SVD变压器接受矩阵，而无需对它们进行密度化
from sklearn.decomposition import TruncatedSVD
tsvd = TruncatedSVD(n_components=2)
# 不对矩阵进行居中处理
tsvd.fit(X)
tsvd.transform(X)
tsvd.explained_variance_ratio_ #总解释比与pca大致类似，但是主成分不同
tsvd.components_
pca.explained_variance_ratio_
pca.components_

#对矩阵进行居中处理，减去特征均值
#结果与原始PCA一致
tsvd.fit(X-X.mean(axis=0))
tsvd.transform(X-X.mean(axis=0))
tsvd.explained_variance_ratio_ 
tsvd.components_
# =============================================================================
# 







#独立成分分析  ICA
# =============================================================================
#
