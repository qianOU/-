1. #### 将浏览器中的全局对象，替换为node中的全局对象

```javascript
 window = global
```

2. #### 导入常用的crypto-js库进行常规加密/解密操作

    ```java
    var CryptoJs = require('crypto-js');
    ```

    

3. #### 利用npm工具进行库管理

    ```
    #npm下载缓慢，所以使用cnpm依托淘宝镜像进行库管理
    npm install -g cnpm --registry=https://registry.npm.taobao.org
    
    cnpm install express #下载express库
    cnpm uninstall express #卸载express库
    
    cnpm ls #查看本地安装的所有库名
    ```

    

4.  查看npm和cnpm的储存位置，好加入环境变量中

    ```
    cnpm ls //查看已安装包的位置
    ```

    