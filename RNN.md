

#### RNN循环神经网络

> ### RNN中有一个好处就是没有明确规定word num，只要求特质数量一致即可，比如说可以通过一个word num的特征迭代得到后面所有的序列

>  ### 1.数据输入形式
>
> ![](D:\保存位置\markdwon笔记图片保存内容\RNN-输入.png)
>
> 其中：word num代表**句子中连续单词个数也即连续时间戳个数**，b代表句子个数即batch，word vec代表单词特征即序列特征【如收盘价，开盘价等】
>
> 两种输入方式都可，第一种是如图中曲线所示站在时间戳的角度观察，推荐第一种

> ### 2.RNN原理
>
> #### 单层的RNN
>
> ![](D:\保存位置\markdwon笔记图片保存内容\逻辑图.png)
>
> #### 两层的RNN
>
> ![](D:\保存位置\markdwon笔记图片保存内容\mult_layer.png)
>
> 在这里h_t为【batch，hidden len】的tensor，其中第二维度代表每个batch上储存hidden_len长度的**记忆**，h_0，初始化为0-tensor。经过计算得到可以输出$\;h_{t+1}$; 即t+1期的记忆输出shape为【batch，hidden len】。
> $$
> 参数的shape比较(其中hidden\;len表示存储记忆的长度)\\
> x_t=[batch, feature\;len]\\
> x = [word\; num/timestamp\;num, bantch, feature\;len]
> \\W_{xh} = [hidden\;len, feature\;len]\\
> h_t = [batch, hidden\;len]\\
> W_{hh} = [hidden\;len, hidden\;len]
> $$
> 
>

> > 实现
> >
> > ```python
> > nn.RNN(input_feature, hidden_size, num_layers=1)
> > 
> > #构建一个输入特征为100维，记忆长度为20的RNN循环网络
> > a = torch.nn.RNN(100, 20)
> > #打印a中参数名称以及相应shape
> > for name, item in dict(a.named_parameters()).items():
> >  print(name, 'shape=', item.shape)
> > 
> > >>  weight_ih_l0 shape= torch.Size([20, 100]) #[hidden_size, feature_size]
> >  weight_hh_l0 shape= torch.Size([20, 20]) #[hidden_Size, hidden_size]
> >  bias_ih_l0 shape= torch.Size([20])#[hidden_size]
> >  bias_hh_l0 shape= torch.Size([20])#[hidden_size]
> > ```
> >
> > #### nn.RNN前向传播过程
> >
> > ![](D:\保存位置\markdwon笔记图片保存内容\nn.RNN.png)
> >
> > 有几点说明：
> >
> > 1. nn.RNN可以对所有输入数据进行处理即不用划分为$x_t$进行训练
> > 2. seq len相当于**句子中连续单词个数**word num
> > 3. ho是初始记忆单位，其后训练过程中要用h_t来进行替代
> > 4. h_t返回的是**所有RNN层最后一个单元**的记忆即h_T
> > 5. out则保存了**RNN最后一层上所有单元**的记忆即【h1，h2,...h_hidden】
> >
> > #### nn.RNNCell
> >
> > ![](D:\保存位置\markdwon笔记图片保存内容\rnncell.png)
> >
> > 几点说明：
> >
> > 1. 与nn.RNN相比，此处相当于每次只提取一个单词进行计算，需要自己循环添加单词进行训练
> >
> > 实现：
> >
> > ```python
> > #单层cell
> > cell1 = nn.RNNCell(100, 20)#feature=100, memory=20
> > h1 = torch.zeros(3, 20) #3为batch， 20为memory
> > for xt in x: #循环添加xt进行训练xt.shape = (batch, feature)
> > 	h1 = cell1(xt, h1) #将得到的xt记忆应用于下个x_t+1
> > print(h1.shape) #[3, 20][batch,  memory]
> > 
> > 
> > 
> > #两层cell
> > cell1 = nn.RNNCell(100, 30)#feature=100, memory=30
> > cell2 = nn.RNNCell(30, 20)#cell1_feature=30, memory=20
> > h1 = torch.zeros(3, 30)
> > h2 = torch.zeross(3, 20)
> > for xt in x:
> > 	h1 = cell1(xt, h1) #将xt的记忆用于x_t+1,同时传导到cell2
> > 	h2 = cell2(h1, h2) #将xt的记忆用于x_t+1
> > print(h2.shape) #[3, 20][batch,  memory]
> > print(h1.shape) #[3, 30][batch,  memory]
> > ```

> ![](D:\保存位置\markdwon笔记图片保存内容\RNN-formula.png)
>
> 注意：因为有$W_R^k$所以RNN在训练过程中，会难以收敛。主要存在**梯度弥散和梯度爆炸的情况**
> $$
> \begin{array}{c|c}
> 名称 & 例子\\
> \hline
> 梯度爆炸 & {1.01}^{365} \approx 37\\
> 梯度弥散 & {0.99}^{365}\approx 0.03\\
> \end{array}
> $$
> 



