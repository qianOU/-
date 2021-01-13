### visdom 神经网络可视化

> #### 安装
>
> 1. pip install visdom
> 2. 打开服务器：python -m visdom.server
> 3. 输入第2步返回的网站

> #### 案列
>
> 1.可视化loss
>
> ```
> from visdom import Visdom
> viz = Visdom()
> #创建初始线，注意顺序为Y,X
> viz.line([0], [0], win='train_loss', opts=dict(title='train loss'))
> #将loss添加进loss下降线中
> viz.line([loss.item()], [global_step], win='train_loss', update='append')
> 
> #绘制多条曲线
> viz = Visdom()
> #同时绘制两条曲线，顺序为y1,y2, x
> viz.line([[0, 0]], [0], win='test', opts=dict(title='test loss&acc', legend=['loss', 'acc']))
> viz.line([[test_loss,correct/len(test_loader.dataset)]], [global_step], win='test', update='append')
> ```
>
> 2.可视化图片
>
> ```
> #可视化图片
> viz = Visdom()
> #数据形式为【B, C, H, W】
> viz.images(data.view(-1, 1, 28, 28), win='x')
> viz.text(str(pred.detach().cpu().numpy()), win='x', opts=dict(title='pred'))
> ```
>
> ![](D:\保存位置\markdwon笔记图片保存内容\visdom.jpg)

## 保存

可视化的时候，可以设置`log_to_filename`属性进行保存数据

```python
vis = Visdom(env="demo", log_to_filename="./visdom.log")
```

如果要重新可视化保存的数据，则直接运行

```python
Visdom.replay_log(log_filename="./visdom.log")
```

这样在启动visdom服务时即可看到之前可视化的数据