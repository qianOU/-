### Pytroch

#### torch

* 向量运算

```
torch.dot（input，other） #点积（内积）#input.dot(other)
torch.cross（input，other）# 外积（外乘）
```

* 范数计算

```python
torch.dist（input, other，p = 2 ） →张量 #也可以用面向对象的写法 input.dist(other, p=2)
torch.norm(input, dim=0)
```

![](D:\保存位置\markdwon笔记图片保存内容\norm.jpg)

* 求特征值，特征向量

```
torch.eig(input, eigenvectors=False, out=None) -> (Tensor, Tensor)
#默认input是对称的，upper=True，代表取对称的input的上三角部分进行计算
torch.symeig(input, eigenvectors=False, upper=True, out=None) -> (Tensor, Tensor)

```

* 弧度转角度

```python
torch.rad2deg（input，out = None ）
```

* 张量的**深拷贝**

```python
tensor.to_mkldnn()
tensor.clone()
```

* 获得**下/上三角矩阵**（可进行**批处理**）

```python
torch.tril(input, diagonal=0, out=None)#下三角
torch.triu(input, diagonal=0, out=None)#上三角
```

* 向0取整

```
torch.trunc（input，out = None ） →张量
```

* 转换类型

```
type（dtype = None，non_blocking = False，** kwargs ） →str或Tensor
```

* 查看Tesnor里面的**种类**，以及**计数**，还有相应的**索引**

```python
tensor.unique（sorted = True，return_inverse = False，return_counts = False，dim = None ）
```

* 按条件替换

```
torch.where（条件，x，y ） →张量， x,y具有广播性质，也可以和input具有一样的结构
```

* 布尔操作，只针对***torch.BoolTensor***

```python
torch.BoolTensor.all（dim，keepdim = False，out = None ） →张量
torch.BoolTensor.any（dim，keepdim = False，out = None ） →张量

#使用all,或则any时必须将tensor利用.bool方法，转换为BoolTensor类型
>>> a = torch.rand(4, 2).bool()
>>> a
tensor([[True, True],
        [True, False],
        [True, True],
        [True, True]], dtype=torch.bool)
>>> a.all(dim=1)
tensor([ True, False,  True,  True], dtype=torch.bool)
```

> Tesnor中的两种高效索引方式
>
> * torch.Tensor.index_select(dim. index:Tensor)
>
> ```
> # 注意index参数必须是Tensor类型
> a = torch.rand(4,3,24,24)
> a.index_select(0, torch.tensor([0,1])) #对a，沿着axis=0的方向，选取index为[0,1]的数据,ret_shape = (2, 3,24, 24)
> ```
>
> * masked_select() #利用掩码进行选取
>
> ```
> # 注意，这样子得到的系列会被flatten为1维数据
> a = torch.rand(3, 4)
> mask = torch.gt(0.5)
> #需要将mask转换为bool类型，通过.type(torch.bool)即可
> b.masked_select(mask.type(torch.bool))
> >> tensor([0.9570, 0.7476, 0.5995, 0.5696, 0.8617])
> ```
>
> * torch.take
>
> ```
> # 在扁平化序列中进行索引,使用时会将input扁平化,并且要求输入的index是扁平化后的index，且以Tensor形式传入
> a = torch.rand(4, 4)
> torch.take(a, torch.tensor([0, 4, 10, 12]))
> >> tensor([0.6476, 0.5557, 0.5038, 0.7713])
> ```
>
> 

> 
>
> 维度变换
>
> * view / reshape
>
> ```
> a = torch.rand(4, 4)
> b = a.reshape(1, 1, 16)
> c = a.view(1, 1, 16)
> # b与c等价
> torch.all((b==c).type(torch.bool))
> ```
>
> * squeeze / unsqueeze
>
> ```
> a = torch.rand(4, 4)
> b = a.reshape(1, 1, 16)
> b.squeeze(dim=1) #ret_shape=[1, 16] 压缩维度大小为1的维度
> a.unsqueeze(dim=0) # ret_shape=[1, 4, 4] 扩展维度
> ```
>
> 
>
> * expand(*shape)/ repeat(num)
>
>     ```python
>     #expand 不做数据复制工作，节约内存,需要输入最终输出的shape
>     b = torch.rand(1,3,4)
>     b.expand(12,3,4) #只能将维度中为1的扩增数据，输出为shape为（12，3，4）
>     b.expand(12,-1,4) #使用-1表示不变 输出shape为（12，3， 4）
>     
>     c = torch.rand([12]).expand(4, 12) #对于一维数据可以直接扩充为二维
>     
>     #repeat 实打实的复制数据，占内存，需要输入每一维度的复制次数
>     b.repeat(4,2,1) #表示对shape[0]中复制4次，shape[1:3]表示复制1次
>     输出shape为(4, 6, 4)
>     ```
>
> * transpose(order_dim)
>
> ```
> #按给定的ord_dim进行交换维度，给出需要交换的两个维度即可
> a = torch.rand(3, 3, 28, 28) #卷积网络输入维度代表 B,C,H,W
> a.transpose(1, 3) #维度调整为 B,W,H,C
> ```
>
> * permute
>
> ```
> permute(order_dim) #order_dim需要完整的dim顺序
> a = torch.rand(3, 3, 28, 28) #卷积网络输入维度代表 B,C,H,W
> a.permute(0， 3， 2， 1) #维度调整为 B,W,H,C
> ```
>
> 

> 广播机制
>
> 1. 在前面插入1维度
> 2. 扩充维度大小为1的到较大的大小
> 3. example:`feature_map + Bias`
>
> ```python
> feature_map :[4, 32, 14, 14]
> Bias: [32, 1, 1] -> [1, 32, 1, 1](从前面插入1维度来扩充维度) ->[4, 32, 14, 14](扩充维度为1的size到较大的大小) 
> 最后进行计算
> ```
>
> ![](D:\保存位置\markdwon笔记图片保存内容\broadcast.jpg)

> 拼接
>
> 1. cat
>
> ```
> # 与np.concatenate, 以及pd.concat很像
> a = torch.rand(4, 32, 8)
> b = torch.rand(8, 32, 8)
> torch.cat([a,b] ,dim=0) #沿着axis=0拼接 ,ret_shape = (12, 32, 8)
> ```
>
> 1. stack
>
> ```
> #插入的时候会扩展维度, 需要拼接的tensor有一致的shape
> a = torch.rand(4, 32, 8)
> b = torch.rand(4, 32, 8)
> answer= torch.stack([a,b] ,dim=0) #ret_shape = (2， 4, 32, 8)
> #其中 answer[0,...]表示a
> answer[1,...]表示b
> ```
>
> 1. split
>
> ```
> b = torch.rand(2， 32, 8)
> #1.通过单元定长来划分
> aa, bb = b.split(1, dim=0) #每个单元的长度为1 aa,bb.shape=(1, 32, 8)
> #2.通过自定义每个单元的长度来划分用list包裹起来
> aa ,bb = b.split([28, 4], dim=1) #前面28个为一组  aa.shape=(2, 28, 8)
> ```
>
> 1. chunk
>
> ```
> #通过定义划分的数量进行切割
> b = torch.rand(2， 32, 8)
> aa, bb = b.chunk(2, dim=0) #沿着axis=0将b切割为均匀2份，若不能均匀切割则最后一份略微少些
> 
> ```

> 统计
>
> * topk(input，largest=True， dim)
>
> ```
> a=tensor([[0.9237, 0.1590, 0.9641, 0.5711, 0.4096, 0.4709, 0.1106, 0.9886],[0.1792, 0.1276, 0.2169, 0.7368, 0.6192, 0.7087, 0.7530, 0.5803], [0.4321, 0.7257, 0.2162, 0.0173, 0.3499, 0.9925, 0.9478, 0.2262],[0.8672, 0.1146, 0.2793, 0.1928, 0.8841, 0.9059, 0.9756, 0.9202]])
> value, index_ = a.topk(3, dim=1)
> # largest=True,默认表示为找寻最大值，当largest=False时，表示找寻最小
> ```
>
> * tornch.Tensor.kthvalue(k, dim， keepdim=False) #返回Tensor中第k小的数字和索引

> 条件替换
>
> * torch.where(condition, x, y) #可以并行计算，可以在GPU中进行
>
> ```
> b = torch.rand(4,3)
> a = b.gt(0.5).float()
> torch.where(b>0.5, a, b) #将b中大于0.5的替换为a中相应的值，否则用b中相应的值替换
> ```
>
> * torch.gather(input, dim, index, out=None) #主要进行查表操作
>
> ```
> label = torch.arange(10) + 100
> idx = torch.randint(0, 9, size=(4,3))
> 
> #根据idx进行查询需要保证idx的维度和label的维度一致，输出结果与idx的shape一致
> torch.gather(label.expand(4, 10), dim=1, index=idx)
> 输出 
> tensor([[105, 102, 107],
>         [102, 108, 101],
>         [104, 106, 103],
>         [102, 101, 103]])
> ```
>
> 



