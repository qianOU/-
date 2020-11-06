### Pytorch过拟合与欠拟合

#### Python前向传播的运算形式

$$
Pytorch中定义前向传播的运算为:\;x@(layer.weight^T)+layer.bias\\
x.shape = [batch, inp]\\
layer.weight.shape = [out, inp]\\
layer.bias.shape = [out]
$$



> ### 初始化
>
> 使用**kai-ming** 初始化方法
>
> ```
> torch.nn.init.kaiming_normal_(tensor) #对权重就地初始化
> ```
>
> 

> ##### 1.数据集划分为训练集，验证集，测试集
>
> ```
> #对训练集进行两部分划分（训练，验证）
> train_db, val_db = torch.utils.data.random_split(train_db, [5000, 1000]) #训练集占5000个，验证集占1000个
> 
> ```
>
> #### 2.k-折交叉验证
>
> ```
> #只需在每个epoch中对数据集进行随机划分即可
> for epoch in range(5):
> 	...
> 	train_db, val_db = torch.utils.data.random_split(train_db, 							[5000, 1000])
> ```
>
> 

> ### 防止过拟合
>
> #### 1.l2-regulization(又称为weight decay):可以压缩每个神经元的权重不要过大
>
> $$
> min\;\left[J(\theta)+\lambda\sum_{i=1}^{n}\theta_i^2\right]
> $$
>
> ```
> #Pytorch中weight decay只支持l2正则，越大正则效果越明显
> optimizer = optim.SGD(net.parameters(), lr=0.01, weight_decay=0.01)
> 
> #手动实现l1正则
> l1_loss = 0
> for param in net.parameters():
> 	l1_loss += torch.sum(torch.abs(param))
> classify_loss = criterion(logits, target) #计算交叉熵，logits必须是概率形式输入
> loss = classify_loss + 0.01*l1_loss #加入l1正则的损失函数值
> 
> optimizer.zero_grad() #梯度清零
> loss.backward()#反向传播
> optimizer.step()#参数迭代优化
> ```
>
> #### 2.Droupout算法
>
> ```
> torch.nn.Dropout(drop_p=0.5) #设定神经元被drop的概率为0.5，默认值0.5
> 
> #训练的时候需要打开net.train()模式，预测的时候需要打开net.eval()模式
> net_dropped = torch.nn.Seqential(
>         torch.nn.Linear(784, 200),
>         torch.nn.Dropout(0.5), #设定dropout
>         torch.ReLU(inplace=True),#因为经过relu变换以后，shape不变所以可以就地进行转换，来节约空间
>         torch.nn.Linear(200, 200),
>         torch.nn.Dropout(0.3), #设定drop_out
>         torch.ReLU(),
>         torch.Linear(200, 10)
>   )
> ```
>
> 

### 训练技巧

#### 1.加入momentum，可以避免陷入局部极值

```
optimizer = optim.SGD(net.parameters(), lr=0.01, momentum=0.9)
```

#### 2.根据训练情况调整lr

```
>>> optimizer = torch.optim.SGD(model.parameters(), lr=0.1, momentum=0.9)
#默认factor=0.1，patient=10，即若patient个epoch，loss都没有下降则降低lr *= factor
>>> scheduler =  torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min')
>>> for epoch in range(10):
>>>     train(...)
>>>     val_loss = validate(...)
>>>     # 注意lr的更新应该在验证之后，并且在权重参数更新之后
>>>     scheduler.step(val_loss)


#还用一类常用的是StepLR
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.1)#每迭代step_size步时，就调整 lr = lr*gamma
```

### BatchNormalization

![](D:\保存位置\markdwon笔记图片保存内容\batch-normaliztion.png)

1. ### 优点：加速训练，更好的表现，稳定性更强

1. 1-d-normallization 将数据规范化，默认服从$N(0,1)$。**默认设定affine为True，即会通过$x=\lambda{x}+\beta$进行转换，增加数据多样性，其中$\lambda,\;\beta$可以通过学习进行调整。$\lambda$储存在layer.weight中，$\beta$存储在layer.bias中。默认$\lambda=1,\beta=0$即输出序列服从$N(0,1)$**

```python
a = torch.rand(1, 3, 32, 32)*10
a = a.view(1, 3, -1)
#1-d BatchNormalization, 3代表通道数
#momentum参数设置为1时running_mean才会计算准确,具体看文档
layer = torch.nn.BatchNorm1d(3, momentum=1)
b = layer(a)
layer.running_mean #返回a中的均值 a.mean(2)
layer.running_var#返回a中的方差 a.var(2)

```

2. 2-d-normaliztion（图像规范化）

    #参事与1-d-normaliztion意思一致

```python
a = torch.rand(1, 3, 32, 32)
#2-d BatchNormalization, 3代表通道数
#momentum参数设置为1时running_mean才会计算准确
layer = torch.nn.BatchNorm2d(3, momentum=1)
b = layer(a)
layer.running_mean #返回a中的均值
a.view(1,3,-1).mean(2) #与上式等价
layer.running_var#返回a中的方差
a.view(1,3,-1).var(2) #与上式等价
```

### 模型保存与加载

```python
# 加载
net.load_state_dict(torch.load('aaa.pkl'))
#保存
torch.save(net.state_dict(), 'aaa.pkl')
```

#### 自己创建类

```python
class MyLine(nn.Module):
    def __init__(self, inp, out):
        super().__init__()
        self.weight = nn.Parameter(torch.rand(out, inp))#自定义初始化weight, shape=[out, inp]
        self.bias = nn.Parameter(torch.rand(out)) #自定义初始化, shape = [out]

    def forward(self, x):
        x = x@self.weight.t() + self.bias #pytorch中定义运算为 x@weight.t()
        return x
```

### 数据增强

> #### 1.Flip
>
> ```python
> from torchversion import transforms
> 
> transforms.RandomHorizontalFlip(p=0.5) #以p=0.5的概率水平翻转
> transforms.RandomVerticalFlip(p=0.5) 
> ```
>
> #### 2.rotate
>
> ```python
> RandomRotation(degrees, resample=False, expand=False, center=None, fill=None)
> 
> transforms.RandomRotation(15) #当输入int时，表示在-15--15度之间随机旋转
> transforms.RandomRotation([0, 90, 180, 270]) #当输入iter-type时，表示在序列之间随机选择一个角度旋转
> ```
>
> #### 3.scale:缩放
>
> ```python
> Resize(size, interpolation=Image.BILINEAR)  #size可以是int也可以是list
> transforms.Resize(32) #将图像沿着中心缩放为32*32大小
> ```
>
> #### 4.crop part：随机裁剪
>
> ```python
> transforms.RandomCrop(size) #size可以是整数也可以是list，即给定切割保留的大小
> 
> transforms.RandomCrop([28, 28])# 将图像在随机位置保存为28*28大小
> ```
>
> ### 组合
>
> ```python
> transforms.Compose([
>      transforms.RandomHorizontalFlip(p=0.5),
>      transforms.RandomVerticalFlip(p=0.5),
>      transforms.RandomRotation(12),
>      transforms.Resize(28),
>      transforms.RandomCrop(24),
>      transforms.ToTensor(), #将其它数据类型转换为Tensor
>      transforms.Normalize(mean=[0.5]*3, std=[0.5]*3) #对每一个图片正则化处理
>       ]
>     )
> ```
>
> 

