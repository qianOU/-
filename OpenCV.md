# OpenCV

## 安装 **opencv 3.4.2.16**

原因：因为这是支持xfeatures2d.SURF_create的最高版本，再升就不支持了

```
pip install opencv-python==3.4.2.16 -i "https://pypi.doubanio.com/simple/"
pip install opencv-contrib-python==3.4.2.16 -i "https://pypi.doubanio.com/simple/"
```

检验安装是否成功

```python
import cv2
sift = cv2.xfeatures2d.SURF_create()
print(cv2.__path__)
```

[参考链接](https://blog.csdn.net/wmm131333/article/details/103359370)