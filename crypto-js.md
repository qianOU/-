1. ### AES + BASE64

```javascript
var CryptoJs = require('crypto-js');
var f = CryptoJs.enc.Utf8.parse("jo8j9wGw%6HbxfFn"); 
var m = CryptoJs.enc.Utf8.parse("0123456789ABCDEF");
function h(t) {
     var e = CryptoJs.enc.Hex.parse(t)
     , n = CryptoJs.enc.Base64.stringify(e)
     , a = CryptoJs.AES.decrypt(n, f, {
                iv: m,
                mode: CryptoJs.mode.CBC,
                padding: CryptoJs.pad.Pkcs7
     })
     , r = a.toString(CryptoJs.enc.Utf8);
     return r.toString()
}
// t 就是返回的加密数据
console.log(h(t))
```

