##  LSTM

<center>此除假设没用使用batch_first选项，即X的shape遵循【seq，b, feature_size】</center>

### nn.LSTM(x, [h_t_1, c_t_1])

![](D:\保存位置\markdwon笔记图片保存内容\LSTM-forward.png)

> 注释：
>
> 1. seq为序列长度，在文字处理中表示的是**句子的单词个数**，在时间序列中则表示的是**使用多长序列进行预测**（比如seq=12，表示用12天的序列进行预测）
> 2. h表示的是**单元输出**，c表示的是**长期记忆**
> 3. out 中存放了最后一层所有单元的输出
> 4. _**LSTM与LSTMCell不同可以一次喂入seq个观测点数据**_

### nn.LSTMCell(x_t, [h_t_1, c_t_1])

![](D:\保存位置\markdwon笔记图片保存内容\lstmcell.png)

> 注释：
>
> 1. **x_t**是一个观测数据，shape为二维的[batch, feature_size] #即为LSTM中的X[t],需要自己每次将seq中的观测喂给模型
> 2. h_t的shape也为二维的**[batch, hidden_size]**

```python
# 利用LSTMCell自己构造两个单元的LSTM
input_ = torch.randn(12, 3, 30)

a = torch.nn.LSTMCell(30, 20)
b =  torch.nn.LSTMCell(20, 10)

h_ly1 = torch.zeros(3, 20)
h_ly2 = torch.zeros(3, 10)
c_ly1 = torch.zeros(3, 20)
c_ly2 = torch.zeros(3, 10)

for x in input_:
    h_ly1, c_ly1 = a(x, [h_ly1, c_ly1])
    h_ly2, c_ly2 = b(h_ly1, [h_ly2, c_ly2])

for name, item in dict(a.named_parameters()).items():
    print('第一个单元', name, 'shape=', item.size())
for name, item in dict(b.named_parameters()).items():
    print('第二个单元', name, 'shape=', item.size())
    
第一个单元 weight_ih shape= torch.Size([80, 30])
第一个单元 weight_hh shape= torch.Size([80, 20])
第一个单元 bias_ih shape= torch.Size([80])
第一个单元 bias_hh shape= torch.Size([80])
第二个单元 weight_ih shape= torch.Size([40, 20])
第二个单元 weight_hh shape= torch.Size([40, 10])
```

### LSTM中的数学推导

![](D:\保存位置\markdwon笔记图片保存内容\lstm中的数学推导.png)

注意与RNN中不同的是$W_{ih}$参数有**4个不同的矩阵**，$W_{hh}$也有四个不同的矩阵，Bias也是同理。**对于RNN则只共用同一组$W_{ih},W_{hh},b_{ih},b_{hh}$**。估计量差四倍的原因见下小节。



### LSTM与RNN中的参数不同点



![](D:\保存位置\markdwon笔记图片保存内容\lstm-参数shape解释图.jpg)

>  几点注意事项：
>
> 1. 注意W的第一维度，其为**RNN**中W第一维度的**4倍input_size**（4*hidden_size）
> 2. W的第二维度保持不变，依旧为input_size
> 3. 若开启**双向循环**，则hidden_size = 2*hidden_size

```python

#### RNN的参数
a = torch.nn.RNNCell(100, 20) #[feature_len, hidden_size]
   ...: #打印a中参数名称以及相应shape
   ...: for name, item in dict(a.named_parameters()).items():
   ...:     print(name, 'shape=', item.shape)

#因为RNN中没用遗忘门，输入门， 输出门
# 所以参数的 w_rnn的 shape为 【hidden_size, feature_len】
#所以 H的shape为 【hidden_size， hidden_size】
weight_ih shape= torch.Size([20, 100]) #[hidden_size, feature_len]
weight_hh shape= torch.Size([20, 20]) #[hidden_size, hidden_size]
bias_ih shape= torch.Size([20]) #[hidden_size]
bias_hh shape= torch.Size([20])#[hidden_size]



#因为LSTM中有遗忘门，输入门， 输出门，以及对X_t要进行tan转换
# 所以W_lstm是4个W_rnn在axis=0上的concat
# 所以参数的 w_ih的 shape为 【4*hidden_size, feature_len】
#同理H_lstm也是类似 为【4*hidden_size, hidden_len】
#bias 为【4*hidden_size】
a = torch.nn.LSTMCell(100, 20)
   ...: #打印a中参数名称以及相应shape
   ...: for name, item in dict(a.named_parameters()).items():
   ...:     print(name, 'shape=', item.shape)
   ...:
weight_ih shape= torch.Size([80, 100])
weight_hh shape= torch.Size([80, 20])
bias_ih shape= torch.Size([80])
bias_hh shape= torch.Size([80])
```

