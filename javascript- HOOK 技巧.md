# javascript- HOOK 技巧

## hook window/document 变量

```javascript
// ==UserScript==
// @name        hook variable
// @namespace   http://tampermonkey.net/
// @version     0.1
// @description try to take over the world!
// @author      You
// @include     *
// @grant       none
// @run-at      document-start
// ==/UserScript==

(function () {
    'use strict';
    var value = window['f'];
    Object.defineProperty(window, 'f', {
        get: function () {
            return value;
        },
        set: function (val) {
            console.log('f=', val);
                debugger;
                return value;
        }
    });
})();
```

## HOOK 某一个cookie的设置过程

```javascript
// ==UserScript==
// @name        Hook Cookie
// @namespace   http://tampermonkey.net/
// @version     0.1
// @description try to take over the world!
// @author      You
// @include     *
// @grant       none
// @run-at      document-start
// ==/UserScript==

(function () {
    'use strict';
    var cookie_cache = document.cookie;
    Object.defineProperty(document, 'cookie', {
        get: function () {
            return cookie_cache;
        },
        set: function (val) {
            debugger;
            console.log('Setting cookie', val);
            // 填写cookie名
            if (val.indexOf('m') != -1) {
                debugger;
            }
            var cookie = val.split(";")[0];
            var ncookie = cookie.split("=");
            var flag = false;
            var cache = cookie_cache.split("; ");
            cache = cache.map(function (a) {
                if (a.split("=")[0] === ncookie[0]) {
                    flag = true;
                    return cookie;
                }
                return a;
            })
            cookie_cache = cache.join("; ");
            if (!flag) {
                cookie_cache += cookie + "; ";
            }
            return cookie_cache;
        }
    });
})();
```

