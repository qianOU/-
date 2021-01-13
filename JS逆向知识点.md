# JS逆向知识点

# 坑

1. Node环境下执行不了全是符号组合的加密JS（JSfuck），全是表情符的（aaencode）以及大量$符号的（jjencode），需要事先解密，不然很容易被try给引入错误的分支，且不报错。
    解密网站：http://codertab.com/JsUnFuck and https://www.qtool.net/decode 

2. 在JS逆向过程中，切记有几点：
    1. 要求精简，非必须的代码可以删除，因为非必须的代码，很可能是反爬相关的
    2. 对于无赋值的函数调用，如果函数内部没有改变全局变量就可以取消调用
    3. 有些js混淆代码，会利用字符串匹配函数进行判断是否人为改变了代码
    4. 关注RegExp，document，window，navigator, global, try ，eval等关键字
    5. 关于ob混淆，最主要的就是经过自执行操作的位移数组，以及解密函数

## 1. btoa : Base64编码

浏览器中的btoa是Base64编码函数，对应的python代码如下：

```python
import base64 
print(base64.b64encode("ynkB1imvbe1Iz5Ij23Ap".encode()).decode())
```

## 2. atob :  Base64解码

```python
import base64
print(base64.b64decode('eW5rQjFpbXZiZTFJejVJajIzQXA=').decode())
```

## 3. MD5编码

python 实现：

```python
import hashlib
hashlib.md5('大撒大撒'.encode()).hexdigest() #返回16进制的字符串
```

## 4. Crypto-js

### 4.1 非对称加密

#### 4.1.1  SHA256（不需要密匙）

```javascript
var CryptoJS = require("crypto-js");
CryptoJS.SHA256('待加密字符串').toString()
```

#### 4.1.2 base64加密(不需要密匙)

```javascript
var CryptoJS = require("crypto-js");
CryptoJS.enc.Base64.stringify(CryptoJS.enc.Utf8.parse('待加密字符串'))
```

#### 4.1.3 base64解密（不需要密匙）

```javascript
var CryptoJS = require("crypto-js");
CryptoJS.enc.Base64.parse("待解密字符串").toString(CryptoJS.enc.Utf8)
```

#### 4.1.4 MD5

```javascript
const crypto = require('crypto');
const hash = crypto.createHash('md5');
// 可任意多次调用update():不过不是覆盖，而是将待加密的字符串进行拼接
hash.update('Hello, nodejs!');
console.log(hash.digest('hex')); // 十六进制：7e1977739c748beac0c0fd14fd26a544
```

#### 4.1.5 Hmac(有密匙)

Hmac算法也是一种哈希算法，它可以利用MD5或SHA1等哈希算法。不同的是，Hmac还需要一个密钥：

```javascript
const crypto = require('crypto');

const hmac = crypto.createHmac('sha256', 'secret-key');

hmac.update('Hello, nodejs!');
console.log(hmac.digest('hex')); 
```

#### 4.1.6 RSA（公钥加密，私钥解密）

```python

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import base64
# rsa加密
public_key = """
-----BEGIN RSA PRIVATE KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAziBz4OOXA+HOa9tBxvr/ARp3p1cAKYD9E8a13CMY1ejrs7Of7jv6cA5nHyaFFapbtZCwwOntCTE1pOqph2JRDGBQEtUYPKxJW6WiXdB/3a3XdPfwpdMW6WSbPP9sINPOOZmDr0RFtftIzVYuMDcsHjB8+lzjIxTaIjD1GLwlpOlJxnZ1S6k3yEfbJdIjkobfoKL/sLh1AKlEX8fuBnFP5LRt7OMiB9k5Cpw8DpdPbn5IkjKKnDv3njzHI+Z+FygUS9HCJ3YeDn9kUtU/v+IlDG+lLIFNC7s2bsvQVsWYyxQLtAi5IdLArxoxo/ZjpT0ghWfm8thMrlK3W8E0veKC1wIDAQAB
-----END RSA PRIVATE KEY-----""".strip()
rsakey = RSA.importKey(public_key)
cipher = PKCS1_v1_5.new(rsakey)
rsa_text =base64.b64encode(cipher.encrypt('加密的密码'.encode('utf8')))
print(rsa_text)

## rsa 解密
private_key = """
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAziBz4OOXA+HOa9tBxvr/ARp3p1cAKYD9E8a13CMY1ejrs7Of7jv6cA5nHyaFFapbtZCwwOntCTE1pOqph2JRDGBQEtUYPKxJW6WiXdB/3a3XdPfwpdMW6WSbPP9sINPOOZmDr0RFtftIzVYuMDcsHjB8+lzjIxTaIjD1GLwlpOlJxnZ1S6k3yEfbJdIjkobfoKL/sLh1AKlEX8fuBnFP5LRt7OMiB9k5Cpw8DpdPbn5IkjKKnDv3njzHI+Z+FygUS9HCJ3YeDn9kUtU/v+IlDG+lLIFNC7s2bsvQVsWYyxQLtAi5IdLArxoxo/ZjpT0ghWfm8thMrlK3W8E0veKC1wIDAQABAoIBABlYdzc3dPnGucWcY8WuVk3R7dWXRo9T64qTfAgyDps69USW+TrniB9gPgDgESw9UuKMBJfsC7f+I40AR9E8Xx/o9d+i8USAoNKSltj3Ssm81wnsdNxHDQGs28PP2oFc2fZOMJmMCRBb8jNBfhNyrUuXBb8ZTdqh9UKQB4s/k1doGV5oK4BFjKlVk62Mh3v1t3Ow29YnuygMYPCa6KuxTrL7EMNpEAAiB1CqReZuWRPV9FzB0pQVzY6wEoESK7Dv/D7NqwlCLjwj8lwebR8a9eYjqRmF7/swWYRNRdRJ/HhaRVrEtRZCd4/B3Kd1rr3Z95rNXd+mk7ruIq2xX8sHphUCgYEAz07q4RtrFGMCDm25dqoZFOnJon7tlyHuvlEI/PqMouneQWBGV8iGLEmabgcxgM8bqhbGeQdiggUE6roC/C8jKqGP8evkO/tGU3nnxYAhenvxA1Je43/mrGK5fZU4I8S+qWSU+54Ajg/eueNFMQZxqbknKxfRYPyDl+aAqp16wzsCgYEA/op+UZru1RN2mC/u9qAOQNhq7DpmO4tKJVNSPVloOqulsFKL8KoH/AGWhfEGfOT0mequwRnVMq4eAwnhk8GfUFhQp23uP3ZAwOryXLQ9/V0f2ICo1lCWvpoclH9SoYlR6i33jI/b/OVMYwu7kEEnIZKMOWKU1K27L2ktv9lLjRUCgYEAtpdAw3J91t/5gLHeB4l8O/JKmWgIZfQKLvB65S7czeUE0Do22ryQiNNvRHfrfxNrv1z+BL2fYvt+wCuD05DE/Zh9i0wEo1wHLiESJd9cHWCrAAz97IzLpIvz6ouSfdadQ9+GZTReMsIBn2Jwn+SYGjAtMoRw82aVlSX9r8iyxt8CgYABGGN2wm3oqM7H1Nz4XrPw/31mStIJy42kH3mpHete5UIvQgusG28xXGhjZygZ/Xo391SNLClIsIschDxeQGUJGXgvYD+4MjARJHGqiHQD1RS//726PlqHs24QDYQzgb3CfjQkfLH7opjzjCdgdYdPk6vay1vMlnrJt3Ak9TBoCQKBgQCFqV8cI1WBMu+AntTAJnHxC0SznBOBts05i4s+fJCLFmaE+iEEKMsQtl1CHjvq8ArkO6yBoV2EJdnZKu+98RyY8NouyjezEGNiCzGs9vb/492SA9Pt3A/v3yo4ss+6abLbyz88fVGQe/Dx5VXGImlT+NcsKEupqd9He2psD6VlVg==
-----END RSA PRIVATE KEY-----""".strip()

pri_key = RSA.importKey(private_key)
cipher = PKCS1_v1_5.new(pri_key)
decode_text = cipher.decrypt(base64.b64decode(rsa_text),0)
print(decode_text.decode('utf8'))
```



### 4.2 对称加密

#### 4.2.1 AES简单加密

AES加密与解密都是依靠同一个密匙,**采用简单加密模式时，每次运行加密结果不同，当加密和解密同时存在于内存中，解密才会正确**，原因是：

> 1. AES加密分为AES-128，AES-192，AES-256三种方法；
> 2. 选用哪种方法取决于密钥的长度，如果密钥的长度为128位，则会使用AES-128进行加密；
> 3. 如果密钥不符合128，192或256，则会按256处理，缺少的位数自动补全；

```javascript
var CryptoJS = require("crypto-js");
CryptoJS.AES.encrypt("Message", "Secret Passphrase").toString() 
//第一次输出结果：U2FsdGVkX1/oDuFr4RShbjkixiIY9tABFhNENeFBmPk=
//第二次输出结果：U2FsdGVkX19v7iHwySpwWNQP+wg38Uurx5SZcxFN9/A=
//第三次输出结果：U2FsdGVkX185ebw0DRa6UHmicbnSb0A+0Ec12C6vcvc=
```

**如果直接在内存中进行保存，还能解密出原文**

#### 4.2.2 AES简答解密

```javascript
var CryptoJS = require("crypto-js");
var encrypt = CryptoJS.AES.encrypt("Message", "Secret Passphrase").toString() //加密
var decrypt = CryptoJS.AES.decrypt('待解密字符串', "Secret Passphrase"); //解密，待解密~ = encrypt
console.log(CryptoJS.enc.Utf8.stringify(decrypt));//输出Message
CryptoJS.AES.decrypt('待解密字符串', 'Secret Passphrase').toString(CryptoJS.enc.Utf8)
```

#### 4.2.3 自定义AES加解密函数

大部分情况下，我们需要自定义aes加解密更多的参数，比如**加密模式、填充**等。
**对于密匙和偏移量暂不支持中文**

```javascript
var CryptoJS = require("crypto-js");

// 待加密字符串
var str = '123456';
// 密钥 16 位，不支持中文
var key = '0123456789abcdef';
// 初始向量 initial vector 16 位，不支持中文
var iv = '0123456789abcdef';
// key 和 iv 可以一致
 
key = CryptoJS.enc.Utf8.parse(key);
iv = CryptoJS.enc.Utf8.parse(iv);

// UTF8解析一下
str =  CryptoJS.enc.Utf8.parse(str);

var encrypted = CryptoJS.AES.encrypt(str, key, {
    iv: iv,
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7
});
 
// 转换为字符串
encrypted = encrypted.toString();
 
// mode 支持 CBC、CFB、CTR、ECB、OFB, 默认 CBC
// padding 支持 Pkcs7、AnsiX923、Iso10126
// NoPadding、ZeroPadding, 默认 Pkcs7, 即 Pkcs5
 
// 解密
var decrypted = CryptoJS.AES.decrypt(encrypted, key, {
    iv: iv,
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7
});
 
// 转换为 utf8 字符串
decrypted = CryptoJS.enc.Utf8.stringify(decrypted);
console.log(encrypted)
console.log(decrypted)
```

## Python 执行js

#### 安装：**`pip install PyExecJS`**
### 使用

```python
import execjs
result=execjs.eval("1+1")
js=execjs.compile('''function sum(i,j){sum=i+j;return sum}''')
result=js.call('sum', 1, 2)
print(result)
```

## express服务框架

```javascript
require("crypto-js")

const express = require('express')
const multipart = require('connect-multiparty');
const multipartMiddleware = multipart();
const bodyParser = require('body-parser');

//导入扣下的js代码
var fun = require('./翻页的m参数.js')

console.log(fun);
//构建实例化对象
const app = express()

//extended:false 不使用第三方模块处理参数，使用Nodejs内置模块querystrinodeng处理
//处理XHR请求时 对于 x-www-form-urlencoded形式提交的数据进行处理
app.use(bodyParser.json()) 
//处理普通请求时 对于 x-www-form-urlencoded形式提交的数据进行处理
app.use(bodyParser.urlencoded({extended:false}))



// 建立get路由
//http://localhost:3000/?timestamp=12345434534
app.get('/', function(req, res){
    timestamp = req.query.timestamp; //传入加密需要的参数
    res.send(fun(parseInt((timestamp)))) //返回加密结果
})


//建立post路由
//使用multipartMiddleware中间件，可以处理已form-data形式提交的数据
// http://localhost:3000
app.post('/encrypt', multipartMiddleware, function(req, res){
    res.send(req.body) // 通过post传递参数
})



//设立监听端口
app.listen(3000)
```

## 杂记

1. 经过标准Base64编码之后，末尾一般会带有**"=“**

2. 使用标准RSA加密时，公钥一般以**”MIJ“**开头

3. 浏览器中的window对象是**不能被覆盖重写的**

4. node中有global对象，**但是浏览器中没有全局global对象**，所以代码中还有可能检测global是否存在作为环境检测

5. **在将js代码利用execjs解析时，最好事先将相应的测试代码注释掉**，因为解析的过程也会执行测试代码，这样很可能会改变初始的全局变量的值。（坑，可见猿人学第9题）

6. **一般hook不住**，大多是代码中通过**覆写 Object.defineProperty 来使得hook失效**

7. **注意检测代码中的try，很有可能会进行环境的判别，从而使得加密算法使用错误的参数，导致错误的结果**

8. 同时 window，navigator， document，eval参数也需要注意，是否对上诉对象进行了操作，尤其是删除window的操作

9. **删除window在浏览器中是无效的但是能正常执行，但是node中会删除我们的生成的window对象**

10. 注意代码中是否**检测了global对象**，正常浏览器是无global对象的，所以需要警惕是否用这个特性作为判别

11. 对于混淆代码，js可以利用**正则表达式**（**RegExp对象，或则拥有test以及compile的对象需要着重关注**）等手法确认相应的js是否被拦截解混淆（**比如出现\n,或者检测函数是否格式化展示**），若是则进行反爬措施，例如利用try引入错误分支，**或则写入对于格式化后的代码而已不是最优的正则表达式，来使得解混淆后的程序卡死，性能奔溃。**

    