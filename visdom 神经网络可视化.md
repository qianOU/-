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

