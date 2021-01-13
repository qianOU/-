## R语音

#### 离线安装外部库

```R
install.packages('./XML.zip', repos=NULL, type='source')
```

#### seq :制造序列

```R
seq(1, 10, by=0.2) #包括10
seq(1, 10, len=100) #包括10
```



#### subset: 获得满足一定条件的子集，返回形式与data一致    

```R
subset(data, condition1 &| condition2 )
```

#### 众数

```R
getmode <- function(v){
   	uniqv<-unique(v) 
    uniqv[which.max(tabulate(match(v, uniqv)))]
}
```

#### 分布函数

1. dnorm(x, mean, sd)

    该函数给出给定平均值和标准差在每个点的概率密度函数值

    ```R
    # Create a sequence of numbers between -10 and 10 incrementing by 0.1.
    x <- seq(-10, 10, by = .1)
    # Choose the mean as 2.5 and standard deviation as 0.5.
    y <- dnorm(x, mean = 2.5, sd = 0.5)
    # Give the chart file a name.
    png(file = "dnorm.png")
    plot(x,y)
    # Save the file.
    dev.off()
    ```

    <img src="D:\研究生\R语音学习资料\dnorm.png" style="zoom:67%;" />

    

2. pnorm(x, mean, sd)

    该函数给出正态分布随机数的概率小于给定数的值。 它也被称为“累积分布函数”

    ```R
    # Create a sequence of numbers between -10 and 10 incrementing by 0.2.
    x <- seq(-10,10,by = .2)
     
    # Choose the mean as 2.5 and standard deviation as 2. 
    y <- pnorm(x, mean = 2.5, sd = 2)
    
    # Give the chart file a name.
    png(file = "pnorm.png")
    
    # Plot the graph.
    plot(x,y)
    
    # Save the file.
    dev.off()
    ```

    <img src="D:\研究生\R语音学习资料\pnorm.png" style="zoom:67%;" />

3. qnorm(p, mean, sd)

    该函数采用概率值，并给出累积值与概率值匹配的数字。

    ```R
    # Create a sequence of probability values incrementing by 0.02.
    x <- seq(0, 1, by = 0.02)
    
    # Choose the mean as 2 and standard deviation as 3.
    y <- qnorm(x, mean = 2, sd = 1)
    
    # Give the chart file a name.
    png(file = "qnorm.png")
    
    # Plot the graph.
    plot(x,y)
    
    # Save the file.
    dev.off()
    ```

    <img src="D:\研究生\R语音学习资料\qnorm.png" style="zoom:67%;" />

4. rnorm(n, mean, sd)

    此函数用于生成分布正常的随机数。 它将样本大小作为输入，并生成许多随机数。

    

```R
# Create a sample of 50 numbers which are normally distributed.
y <- rnorm(1500)

# Give the chart file a name.
png(file = "rnorm.png")

# Plot the histogram for this sample.
hist(y, main = "Normal DIstribution")

# Save the file.
dev.off()
```

<img src="D:\研究生\R语音学习资料\rnorm.png" style="zoom:67%;" />

#### 分布函数总类

| 正态分布 | norm  |  dnorm(x, mean, std)  |
| :------: | :---: | :-------------------: |
| 二项分布 | binom | dbinom(x, size, prob) |
|          |       |                       |

## &与&&的区别

```
对于标量计算结果是一致的
TRUE & FALSE == TRUE && FALSE
对于向量结果不一致
c(TRUE, FALSE) & C(TRUE, TRUE) #c(TRUE, FALSE)
c(TRUE, FALSE) && C(TRUE, TRUE) #TRUE 即第一个元素的逻辑与结果，这样子确保了返回的是标量
```

