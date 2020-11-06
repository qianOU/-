<center><font size=10>git操作手册</center>

## 创建版本库

* *创建用户名和用户邮箱*

```git
git config --global user.name "Morvan Zhou"  
git config --global user.email "hhj@163.com"
```

* 文件状态图

![](D:\保存位置\markdwon笔记图片保存内容\git-status.png)

* 常用命令

```
git init #在这个文件夹中建立 git 的管理文件
# Initialized empty Git repository in /Users/MorvanZhou/Desktop/gitTUT/.git/

git status #查看文件状态

ls -a #查看文件夹中所有文件

#如果修改了文件，则文件状态为unstaged。如果想要保存想要首先使用add把它添加进版本库（staged）
git add 1.py 
git add . #提交项目中所有文件

#第二部就是提交改变（commit）利用-m留下提交信息
git commit -m "create 1.py" 

git commit . -m "commit all " #提交所有的改变

#如果改变的文件之前已经提交过，则再次对其进行更改时可以直接用-am合并add和commit操作
git commit -am "skip add, direct commit" 

#显示修改日志
git log    #detail
git log --oneline   #simple discribe
git log --oneline --graph #打印日志的同时，绘制分支的日志的情况

#查看文件具体的变化
#如果只是修改了文件，还没有add操作则可以利用git diff 查看文件中做了哪些变化
git diff
#如果只是修改了文件，并且add操作但是没有commit则可以利用git diff --cached 查看文件中的变化
git diff --cached

```

## 回到从前（reset）

```
#将 2.py的改变合并到上一个commit中，并不创建新的commit
git add 2.py
git commit -amend --no-edit ## "--no-edit": 不编辑, 直接合并到上一个 commit

#reset 回到add之前
#有时我们添加add了修改, 但是又后悔, 并想补充一些内容再add这时, 我们有一种方式可以回到add之前
git add 1.py
git reset 1.py


#reset 回到commit之前(通过commit的HEAD指针)
#方式一 使用 HEAD^ (n个^表示回到之前n个commit)
git reset --hard head^^
#方式二 通过指针id即commit id
git reset --hard c6762a1

#通过git reflog 可以打印人为操作的所有commit的head
git reflog
```

* 使用checkout 让单个文件回到过去

```
#仅仅要对 1.py 进行回到过去操作, 回到 c6762a1 这一个 commit时的1.py
git checkout c6762a1 -- 1.py   #注意更改后，一定记得add和commit操作

```

## 分支 branch

* merge 原理

![](D:\保存位置\markdwon笔记图片保存内容\merge.png)

```
#使用分支技术可以得到互不相干的版本

git log --oneline --graph #打印日志的同时，绘制分支的日志的情况

#使用branch 创建dev分支
git branch dev #建立dev分支
git branch #查看所有分支以及当前处于的分支

#切换分支
git checkout dev #将版本转换到dev分支中

#使用 checkout -b + 分支名, 就能直接创建和切换到新建的分支
git checkout -b dev2

#将dev版本中的修改推送到master（默认）主版本中
git checkout master #切换回master
git merge dev #将dev合并到master中,不保留merge的commit信息
#将dev合并到master中，利用--no-ff命令 同时保留merge的commit信息
git merge --no-ff -m "keep merge info" dev

```

* 使用rebase分支合并

![](D:\保存位置\markdwon笔记图片保存内容\rebase.png)

```
git checkout master
git rebase dev
#若文件冲突时
git branch #HEAD 并没有指向 master 或者 dev, 而是停在了 rebase 模式上
#手动更改冲突部分然后执行 git add 和 git rebase --continue 就完成了 rebase 的操作了.
git commit -am "solve rebase conflict"
git rebase --continue
```

* 临时修改

```
 git checkout dev #假定在dev上进行开发
 git stash #将未被add和commit的文件暂时保存起来
 git checkout -b boss #做其它任务
 git checkout dev #完成任务返回开发板块
 git stash list    # 查看在 stash 中的缓存
 git stash pop #恢复暂存的工作
```

## 与github进行代码管理

> ## SSH
>
> ##### 1 .查看是否配置过密钥
>
> ```
> cd ~/.ssh #如果显示没有文件，则需要重新创立
> ```
>
> ##### 进行创建（之后不需要输入，一直enter即可）
>
> ```
> ssh-keygen -t rsa -C "youremail@example.com"
> ```
>
> ##### 查看你生成的公钥
>
> ```
> cat ~/.ssh/id_rsa.pub
> ```
>
> ##### 将公钥输入到github中
>
> ![](D:\保存位置\markdwon笔记图片保存内容\github_ssh.jpg)
>
> ##### 验证key是否和github产生联系/（yes）
>
> ```
> ssh -T git@github.com
> ```
>
> ##### 克隆代码到本地（选择**SSH**链接）
>
> ```
> git clone git@gitee.com:cjty/nodejs.git
> ```
>
> #### 重新配置只需要将.ssh文件改删除即可





```
# 连接本地版本库
git remote add origin https://github.com/MorvanZhou/git-demo.git #网站为github在线版本需要自己创立
git push -u origin master     # 推送本地 master 去 origin
git push -u origin dev        # 推送本地 dev  去 origin
 
#推送修改
git checkout dev
git add 3.py
git commit  -m "new 3.py"
git push -u orign dev
```



## 用户名修改

1. ##### 修改密码

    git config --global credential.helper store (输入这个命令后,以后只要在输入一次用户名密码)

2. ##### 查看用户名和邮箱地址：

    ```
    $ git config user.name
    $ git config user.email
    ```

3. ##### 修改用户名和邮箱地址：

    ```
    $ git config --global user.name "username"
    $ git config --global user.email "email"
    ```

