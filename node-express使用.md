# express框架

## 导入插件

```javascript
const express = require('express')
const multipart = require('connect-multiparty');
const multipartMiddleware = multipart();
const bodyParser = require('body-parser');
```

## 实例化

```javascript
//构建实例化对象
const app = express()

//extended:false 不使用第三方模块处理参数，使用Nodejs内置模块querystring处理
//处理XHR请求时 对于 x-www-form-urlencoded形式提交的数据进行处理
app.use(bodyParser.json()) 
//处理普通请求时 对于 x-www-form-urlencoded形式提交的数据进行处理
app.use(bodyParser.urlencoded({extended:false}))


```

## 建立路由

```javascript

// 建立get路由
app.get('/', function(req, res){
    // res.send(req.query)
    res.send('hello world')
})


//建立post路由
//使用multipartMiddleware中间件，可以处理已form-data形式提交的数据
app.post('/sign', multipartMiddleware, function(req, res){
    res.send(req.body)
    // res.send('hello world')
})


//导入扣下的js代码
const fun = require('./翻页的m参数.js')

// post提交的数据
data = {"func": 'fun("%s")'}

//参数加密接口
app.post('/encrypt', multipartMiddleware, function(req, res){
    res.send(eval(req.body.func))
    
})


//设立监听端口
app.listen(3000)
```

## Python 模拟请求

```python
import pandas
from datetime import datetime
import requests

time = int(datetime.now().timestamp()*1000)
url = 'http://127.0.0.1:3000/encrypt'

data = {"func": 'fun("%s")'}

response = requests.post(url, data=data) #使用post来提交参数，可以保证特殊字符（&%）不被处理
print(response.text + ('|%d' % (time/1000)))  #得到加密结果
```

## 调试的时候可以用postman进行测试