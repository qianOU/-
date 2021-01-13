# Docker

1.将应用和环境打包成一个镜像

## Docker 的常用命令

```shell
docker version #显示docker版本信息
docker info #显示系统级信息，包括容器和镜像的数量
docker 命令 --help #帮助命令
```

### 镜像命令

1. docker images #查看镜像对象

```shell
  -a, --all             Show all images
  -q, --quiet           Only show image IDs
```

2. docker search #搜索镜像

```shell
-f  设置过滤条件
--filter=STARS=3000 #搜索star大于3000的镜像
```

3. docker pull 下载镜像

```shell
docker pull sql #默认下载latest即最新版
docker pull 镜像 [:tag] 指定tag，即指定镜像版本
```

4. docker rmi 删除镜像

```shell
docker rmi -f img_id #删除指定镜像
docker rmi -f img_id1 img_id2 #删除指定多个镜像
docker rmi -f $(docker images -aq) #删除全部镜像
```

### 容器命令

*说明：* 有了镜像才可以创建容器，linux，下载centos镜像学习

```shell
docker pull centos
```

1. 新建容器并且启动

```shell
docker run [可选参数] image
#参数说明
--name=Name 容器名字， 用来区分容器
-d  后台方式运行
-it 使用交互方式运行，进入容器查看内容
-p（小写） 指定容器的端口 具体：主机端口:容器端口
-P(大写) 随机指定端口

#测试
docker run --name=centos1 -it centos /bin/bash #交互式启动容器
[root@1a917260b3ed /]# ls  #查看容器中（centos）的命令，1a917260b3ed为容器id名
bin  dev  etc  home  lib  lib64  lost+found  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
[root@1a917260b3ed /]# exit #退出容器到主机

```

2. 列出所有的运行的命令

```shell
docker ps #查看当前运行的容器
-a #列出运行的容器，包括历史运行
-n=? #显示最近创建的?个容器
-q #只显示容器的编号id

```

3. 退出容器

```shell
exit #容器停止并推出
ctrl + p + q #容器不停止退出
```

4. 删除容器

```shell
docker rm 容器id #不能删除运行的容器，强制删除使用参数 -f
docker rm -f $(docker ps -aq) #删除所有的容器
docker ps -a -q|xargs docker rm #删除所有的容器
```

5. 启动和停止容器

``` shell
docker start 容器id #启动容器
docker restart 容器id #重启容器
docker stop 容器id #停止当前运行容器
docker kill 容器id #强制停止容器
```

### 常用的其它命令

1.  后台启动容器

``` shell
# 后台启动容器
docker run -d centos
# 问题 docker ps 发现centos停止了，没有后台继续运行
#常见的坑：docker容器使用后台运行，就必须要有一个前台进程进行联系。docker发现没有前台进程，就会自动停止
```

2.  查看日志

``` shell
docker logs -tf 容器id #显示某个容器的运行日志
-tf #格式化显示日志包括时间time,and format
--tail number #要显示的日志条数
docker logs -tf --tail 10 容器id #显示某个容器的最新10条运行日志
```

3. 查看容器中的进程信息

``` shell
docker top 容器id #查看容器内部的进程信息
# pid 程序进程号，ppid 程序的父进程号
```

4.  查看容器中的内部信息

``` shell
docker inspect 容器id #可以查看详细的容器信息
## 元数据
[
    {
        "Id": "229bffaefc0ff494b47594ee4423c607c6e8b43475380ad05e4756564e079ad6",
        "Created": "2021-01-12T14:49:09.0266276Z",
        "Path": "/bin/bash",
        "Args": [],
        "State": {
            "Status": "running",
            "Running": true,
            "Paused": false,
            "Restarting": false,
            "OOMKilled": false,
            "Dead": false,
            "Pid": 1090,
            "ExitCode": 0,
            "Error": "",
            "StartedAt": "2021-01-12T14:49:09.4294162Z",
            "FinishedAt": "0001-01-01T00:00:00Z"
        },
        "Image": "sha256:300e315adb2f96afe5f0b2780b87f28ae95231fe3bdd1e16b9ba606307728f55",
        "ResolvConfPath": "/var/lib/docker/containers/229bffaefc0ff494b47594ee4423c607c6e8b43475380ad05e4756564e079ad6/resolv.conf",
        "HostnamePath": "/var/lib/docker/containers/229bffaefc0ff494b47594ee4423c607c6e8b43475380ad05e4756564e079ad6/hostname",
        "HostsPath": "/var/lib/docker/containers/229bffaefc0ff494b47594ee4423c607c6e8b43475380ad05e4756564e079ad6/hosts",
        "LogPath": "/var/lib/docker/containers/229bffaefc0ff494b47594ee4423c607c6e8b43475380ad05e4756564e079ad6/229bffaefc0ff494b47594ee4423c607c6e8b43475380ad05e4756564e079ad6-json.log",
        "Name": "/competent_rhodes",
        "RestartCount": 0,
        "Driver": "overlay2",
        "Platform": "linux",
        "MountLabel": "",
        "ProcessLabel": "",
        "AppArmorProfile": "",
        "ExecIDs": null,
        "HostConfig": {
            "Binds": null,
            "ContainerIDFile": "",
            "LogConfig": {
                "Type": "json-file",
                "Config": {}
            },
            "NetworkMode": "default",
            "PortBindings": {},
            "RestartPolicy": {
                "Name": "no",
                "MaximumRetryCount": 0
            },
            "AutoRemove": false,
            "VolumeDriver": "",
            "VolumesFrom": null,
            "CapAdd": null,
            "CapDrop": null,
            "Capabilities": null,
            "Dns": [],
            "DnsOptions": [],
            "DnsSearch": [],
            "ExtraHosts": null,
            "GroupAdd": null,
            "IpcMode": "private",
            "Cgroup": "",
            "Links": null,
            "OomScoreAdj": 0,
            "PidMode": "",
            "Privileged": false,
            "PublishAllPorts": false,
            "ReadonlyRootfs": false,
            "SecurityOpt": null,
            "UTSMode": "",
            "UsernsMode": "",
            "ShmSize": 67108864,
            "Runtime": "runc",
            "ConsoleSize": [
                30,
                120
            ],
            "Isolation": "",
            "CpuShares": 0,
            "Memory": 0,
            "NanoCpus": 0,
            "CgroupParent": "",
            "BlkioWeight": 0,
            "BlkioWeightDevice": [],
            "BlkioDeviceReadBps": null,
            "BlkioDeviceWriteBps": null,
            "BlkioDeviceReadIOps": null,
            "BlkioDeviceWriteIOps": null,
            "CpuPeriod": 0,
            "CpuQuota": 0,
            "CpuRealtimePeriod": 0,
            "CpuRealtimeRuntime": 0,
            "CpusetCpus": "",
            "CpusetMems": "",
            "Devices": [],
            "DeviceCgroupRules": null,
            "DeviceRequests": null,
            "KernelMemory": 0,
            "KernelMemoryTCP": 0,
            "MemoryReservation": 0,
            "MemorySwap": 0,
            "MemorySwappiness": null,
            "OomKillDisable": false,
            "PidsLimit": null,
            "Ulimits": null,
            "CpuCount": 0,
            "CpuPercent": 0,
            "IOMaximumIOps": 0,
            "IOMaximumBandwidth": 0,
            "MaskedPaths": [
                "/proc/asound",
                "/proc/acpi",
                "/proc/kcore",
                "/proc/keys",
                "/proc/latency_stats",
                "/proc/timer_list",
                "/proc/timer_stats",
                "/proc/sched_debug",
                "/proc/scsi",
                "/sys/firmware"
            ],
            "ReadonlyPaths": [
                "/proc/bus",
                "/proc/fs",
                "/proc/irq",
                "/proc/sys",
                "/proc/sysrq-trigger"
            ]
        },
        "GraphDriver": {
            "Data": {
                "LowerDir": "/var/lib/docker/overlay2/aea7230ced412dc56bb35b8fbf4a5408609b2d140bb05dca3a0dd138e47376f4-init/diff:/var/lib/docker/overlay2/8df9ca71bc843f0a606a897af9e0efafdcc56f4cf1120a4cf266c37e674d96b2/diff",
                "MergedDir": "/var/lib/docker/overlay2/aea7230ced412dc56bb35b8fbf4a5408609b2d140bb05dca3a0dd138e47376f4/merged",
                "UpperDir": "/var/lib/docker/overlay2/aea7230ced412dc56bb35b8fbf4a5408609b2d140bb05dca3a0dd138e47376f4/diff",
                "WorkDir": "/var/lib/docker/overlay2/aea7230ced412dc56bb35b8fbf4a5408609b2d140bb05dca3a0dd138e47376f4/work"
            },
            "Name": "overlay2"
        },
        "Mounts": [],
        "Config": {
            "Hostname": "229bffaefc0f",
            "Domainname": "",
            "User": "",
            "AttachStdin": true,
            "AttachStdout": true,
            "AttachStderr": true,
            "Tty": true,
            "OpenStdin": true,
            "StdinOnce": true,
            "Env": [
                "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
            ],
            "Cmd": [
                "/bin/bash"
            ],
            "Image": "centos",
            "Volumes": null,
            "WorkingDir": "",
            "Entrypoint": null,
            "OnBuild": null,
            "Labels": {
                "org.label-schema.build-date": "20201204",
                "org.label-schema.license": "GPLv2",
                "org.label-schema.name": "CentOS Base Image",
                "org.label-schema.schema-version": "1.0",
                "org.label-schema.vendor": "CentOS"
            }
        },
        "NetworkSettings": {
            "Bridge": "",
            "SandboxID": "483f5571dbbcd764d3095722a0f7f82e658d90a06a5709b9c0e65ebb368f6594",
            "HairpinMode": false,
            "LinkLocalIPv6Address": "",
            "LinkLocalIPv6PrefixLen": 0,
            "Ports": {},
            "SandboxKey": "/var/run/docker/netns/483f5571dbbc",
            "SecondaryIPAddresses": null,
            "SecondaryIPv6Addresses": null,
            "EndpointID": "ca09dced1127eb580d20338f6c45efdc5acc3d5a4546ac43264861b9665b9920",
            "Gateway": "172.17.0.1",
            "GlobalIPv6Address": "",
            "GlobalIPv6PrefixLen": 0,
            "IPAddress": "172.17.0.2",
            "IPPrefixLen": 16,
            "IPv6Gateway": "",
            "MacAddress": "02:42:ac:11:00:02",
            "Networks": {
                "bridge": {
                    "IPAMConfig": null,
                    "Links": null,
                    "Aliases": null,
                    "NetworkID": "4f039985666eeccd66661fa4222cb3bcab6400341bb13fbbc5fecccbdc34d15c",
                    "EndpointID": "ca09dced1127eb580d20338f6c45efdc5acc3d5a4546ac43264861b9665b9920",
                    "Gateway": "172.17.0.1",
                    "IPAddress": "172.17.0.2",
                    "IPPrefixLen": 16,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "MacAddress": "02:42:ac:11:00:02",
                    "DriverOpts": null
                }
            }
        }
    }
]

```

5. 进入当前正在运行的容器

```shell
# 容器一般在后台运行，需要进入容器，修改配置

#命令
#方式1
docker exec -it 容器id bashshell
docker exec -it 229bffaefc0f /bin/bash

#方式2
docker attach 容器id

#区别
#docker exec #相当于进入容器后开启一个新的终端，可以在里面操作（常用）
#dcoker attach #相当于进入容器正在执行的终端，不会启动新的进程
```

6. 从容器内拷贝文件到主机上

``` shell
docker cp 容器id:容器内路径  目的的主机路径

#example
PS D:\桌面> docker attach 6cff01677ce0    #进入正在运行的容器                                           
[root@6cff01677ce0 /]# cd /home 
[root@6cff01677ce0 home]# ls
[root@6cff01677ce0 home]# touch a.txt #创建a.txt文件
[root@6cff01677ce0 home]# ls
a.txt
[root@6cff01677ce0 home]# exit #退出容器
exit

PS D:\桌面> docker ps -a     #查看容器id                                                              
CONTAINER ID   IMAGE    COMMAND            CREATED                STATUS   
6cff01677ce0   centos   "/bin/bash"    10 minutes ago   Exited (0) 13 seconds ago                     

PS D:\桌面> docker cp 6cff01677ce0:/home/a.txt .        #将容器内部的a.txt 复制到当前目录下    


##拷贝只是一个手动过程，未来我们使用-v 卷的技术，可以实现目录之间的互通
```

7. 查看容器消耗的资源以及限制容器的内存

```shell
docker status #查看统计结果
docker run的-e参数可以限制资源占用
```

### 实战一 ：安装nginx

```shell
docker search nginx #搜索
docker pull nginx #下载
docker run -d --name nginx01 -p 3344:80 nginx #启动容器
docker ps #查看是否启动
curl localhost:3344 #测试

docker exec -it nginx01 /bin/bash #进入容器
```

### 实战二 ：安装tomcat

```shell
docker run -it tomcat:9.0 #如果本地没有，会自动pull
参数 --rm #表示在用完容器后，自动删除镜像（docker ps -a 无法查询到）


docker pull tomcat:9.0 #下载tomcat
docker images #查看镜像
docker run -d -p 3555:8080 --name tomcat01 tomcat #启动
```

### docker镜像原理 

1. **镜像层是只读的不可被修改，我们修改的是容器层。**最后可以将修改后的容器打包成自己的镜像。

![image-20210113111732202](D:\桌面\学习记录\markdwon笔记图片保存内容\image-20210113111732202.png)

### commit镜像

**如果你想要保存当前容器的状态，就可以通过commit来提交，获得一个镜像**

```shell
docker commit #提交镜像成为一个新的副本

#命令格式
docker commit -m="提交的信息" -a="作者" 容器id 目标镜像名 [:TAG]

#实战
#1. 启动一个tomcat
docker run -d -p 8080:8080 tomcat
#2.发现这个默认的tomcat是没有webapps应用，这主要是因为官方的镜像阉割过
docker exec -it 229bffaefc0f /bin/bash
cd webapps
ls #为空
#3.自docker己进入容器，并且进行创建基本的webapps
cd ..
cp -r webapps.dist/* webapps
cd webapps
ls #里面有了基础文件
#4. 将我们操作过的容器通过commit提交为一个镜像！以后就可以直接使用修改过的镜像
docker commit -m="add webapps" -a="hhj" 229bffaefc0f tomcato2:1.0 #自己创建了一个tomcat副本，版本设位1.0
docker images #可以查到相应的信息
```

## 容器数据卷技术

==需求：数据可以持久化，不用保存在容器中。本质是目录的挂载==
**总结一句话：使用卷技术，就是为了容器的持久化和同步操作。当然容器间也是可以数据共享的**
**==使用卷技术可以使得容器和主机共享同一块目录下的数据，两者对目录的操作都会影响另外一方的使用==**（前提是容器不要被删除）
**假设我们删除了容器，我们挂载到本地的数据卷依旧没有丢失，这就实现了容器数据的持久化**

### 使用数据卷

```shell
#方式一：直接使用命令来挂载 -v
docker run -it -v -p 主机目录:容器目录 镜像名字
#eg 
docker run -it -v ./test:/home centos /bin/bash   #将主机的test文件夹与centos镜像开启的容器中的home文件进行绑定
docker inspect 
```

![image-20210113124217324](D:\桌面\学习记录\markdwon笔记图片保存内容\image-20210113124217324.png)

### 实战MySQL

```shell
docker pull mysql:5.7  #下载mysql

#启动镜像，构成容器
-d 后台运行
-p 端口映射
-v 卷挂载 #可以挂载多个目录映射
-e 环境配置 #mysql需要配置密码
-- name 容器名字 #给定容器名称，便于后续查询/删除容器等操作
docker run -d -p 3310:3306 -v D:/桌面/mysql/conf:/etc/mysql/conf.d -v D:/桌面/mysql/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 --name mysql01 mysql:5.7

#假设我们删除了容器，我们挂载到本地的数据卷依旧没有丢失，这就实现了容器数据的持久化
```

### 具名挂载与匿名挂载

以==nginx==镜像为例

```shell
#匿名挂载，在-v中只指定容器中的挂载目录，没有写容器外部的路径
docker run --name nginx-test -p 8080:80 -d -v /etc/nginx nginx

#使用docker volume 可以查看卷挂载的信息
docker volume ls
#匿名挂载信息
DRIVER               VOLUME NAME
local  f66e15f8f980b6297669f59ef280402f13581d870ab4b38e3d63bd11de577a69


##具名挂载,指定具体的名字，但是不是目录与容器目录进行绑定
#通过 -v 卷名:容器内路径
docker run --name nginx-test -p 8080:80 -d -v juming_nginx:/etc/nginx nginx
docker volume ls
DRIVER    VOLUME NAME
local   f66e15f8f980b6297669f59ef280402f13581d870ab4b38e3d63bd11de577a69 #匿名
local     juming_nginx #具名
local     test #使用主机目录
#查看一下这个卷
docker volume inspect  juming_nginx
```

![image-20210113133455287](D:\桌面\学习记录\markdwon笔记图片保存内容\image-20210113133455287.png)

**所有的docker容器内的卷，没有指定目录的情况下都是在`/var/lib/docker/volumes/juming_nginx/_data`**
**我们通过具名挂载可以方便的找到我们的一个卷，大多数情况下我们都使用`具名挂载`**

```shell
#如何确定是具名挂载还是匿名挂载，还是指定路径挂载
-v 容器内路径 #匿名挂载
-v 卷名:容器内路径 #具名挂载
-v 宿主机路径:容器内路径 #指定路径挂载
```

### 卷管理与容器权限

```shell
# docker volume 参数
  create      Create a volume
  inspect     Display detailed information on one or more volumes
  ls          List volumes
  prune       Remove all unused local volumes
  rm          Remove one or more volumes
```

==权限==

```shell
#通过 -v 后面添加ro与rw改变读写权限
ro   read—only #只读
rw   read and write #读写（默认情况）
#设置为ro时，容器只有读取权限，无法修改挂载出来的数据，修改内容需要主机完成
docker run --name nginx-test -p 8080:80 -d -v juming_nginx:/etc/nginx:ro nginx
#设置rw，容器具有读写权限，可以更改挂载出来的数据
docker run --name nginx-test -p 8080:80 -d -v juming_nginx:/etc/nginx:rw nginx

#ro 只要看到ro就说明这个路径只能通过宿主机来操作，容器内部无法操作！
```

### 初始Dockerfile

dockerfile是用来构建docker镜像的构建文件！类似命令脚本
通过这个脚本可以生成镜像，**镜像是一层一层的，脚本每一条命令都是一层。**

```shell
# 卷挂载的方式二
# 创建一个dockerfile文件，名字可以随机，推荐使用Dockerfile
#文件中的 指令（大写）内容
FROM centos
VOLUME ["volume01"] #指定容器内的目录需要被挂载
CMD echo "----end---"
CMD /bin/bash

#运行Dockerfile文件
-f 指定dockfile文件位置
-t 指定传建的镜像名称和tag版本
最后需要传入路径path。. 代表当前路径
docker build -f ./Dockerfile -t hhj/centos:1.0 .
```

![image-20210113143739528](D:\桌面\学习记录\markdwon笔记图片保存内容\image-20210113143739528.png)

**这个卷和外部一定有一个同步目录！**

```shell
FROM centos
VOLUME ["volume01"] #匿名挂载形式
CMD echo "----end---"
CMD /bin/bash
```

```shell
#查看挂载信息
docker inspect  cc83b87d4024  # 容器id
```

![image-20210113144402809](D:\桌面\学习记录\markdwon笔记图片保存内容\image-20210113144402809.png)

这种方式是在未来使用非常多的，因为我们通常会构建自己的镜像。
**假设构建镜像时间没有挂载卷，就需要手动镜像挂载-v 卷名:容器内路径**

### 数据卷容器

**重要参数：==--volumes-from==**

![image-20210113162305791](D:\桌面\学习记录\markdwon笔记图片保存内容\image-20210113162305791.png)

```shell
#测试：利用前面创建的自带卷的hhj/images进行测试 
```

第一个容器：

![image-20210113162758841](D:\桌面\学习记录\markdwon笔记图片保存内容\image-20210113162758841.png)

第二个容器：

![image-20210113163041869](D:\桌面\学习记录\markdwon笔记图片保存内容\image-20210113163041869.png)

第三个容器：

![image-20210113163146248](D:\桌面\学习记录\markdwon笔记图片保存内容\image-20210113163146248.png)

增删改查：
![image-20210113163909685](D:\桌面\学习记录\markdwon笔记图片保存内容\image-20210113163909685.png)

卷名的重挂载

![image-20210113165905682](D:\桌面\学习记录\markdwon笔记图片保存内容\image-20210113165905682.png)

```shell
#查看卷信息
docker volume ls                                                                                        DRIVER    VOLUME NAME
local     d776efb427688276821cb67911813439ddb6ebbfd2c24b8eb44c04c2db33e5c9 #上述三个docker容器确实挂载在同一个数据卷
#测试 删除docker01之后，docker02与docker03是否还能继续访问文件？ ans：yes
```

![image-20210113164159912](D:\桌面\学习记录\markdwon笔记图片保存内容\image-20210113164159912.png)

**实战：多个mysql同步数据**

```shell
#使用匿名挂载
docker run -d -p 3310:3306 -v/etc/mysql/conf.d -v /var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 --name mysql01 mysql:5.7
docker run -d -p 3310:3306 -v/etc/mysql/conf.d  --name mysql02 --volumes-from mysql01 mysql:5.7
#这就实现了两个mysql的数据同步
```

**结论**

1. **容器之间配置信息的传递，数据卷容器的生命周期一致持续到没有容器使用为止**
2. **数据卷不会自己删除，可以使用docker inspect查看保存的位置。在这之后可以使用卷名重新怪载到新的容器上**
3. **但是一旦你持久化到本地，这个时候。本地的数据是不会删除的**

