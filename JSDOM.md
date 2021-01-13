```javascript
// 利用jsdom补全浏览器环境
const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const dom = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`);

var window = dom.window;
var document = dom.window.document;
var navigator = dom.window.navigator;

location = {
    'href':'https://www.baidu.com'
}
```

