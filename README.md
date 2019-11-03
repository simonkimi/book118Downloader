# 记一次book118破解进行免费下载的过程

## 序 
学期过半, 是时候补一补马克思主义原理的课了, 想整一本电子书pdf, 但是这本书很难找, 只有book118有, 但是我寻思这个也是网络搜集, 甚至有别人的名字写在上面, 版权也不是他家的, 那么问题不大, 看看能不能白嫖
示例地址: https://max.book118.com/html/2018/0725/7143031033001141.shtm

![在这里插入图片描述](https://img-blog.csdnimg.cn/20191101001451312.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQyNDM2MTc2,size_16,color_FFFFFF,t_70)

## 思路
这个pdf全文可读, 如果无法下载的话, 我可以把每一面的图片下载下来, 然后合成一个pdf并进行ocr即可, 那么当前任务便简化为如何下载每一张图片


## 开始分析

### 0x01 取得真实地址
 看看能不能直接从源代码中找到下载地址, 点击同意开始预览, 按下F12审查元素, 发现整个页面是放在一个iframe里的, 那直接从src定位到真实的地址, 为 https://max.book118.com//index.php?g=Home&m=NewView&a=index&aid=7143031033001141&v=20190917
 ![在这里插入图片描述](https://img-blog.csdnimg.cn/20191101001539759.png)
 
 
 ### 0x02 分析网站源代码
 在新打开的页面内, 按继续阅读后按F12审查元素, 发现所有图片均为懒加载. 在没有加载时是没有src的, 即不会加载图片. 当加载图片后, img内会多出属性src和**data-src**且它们相同, 毋庸置疑, 这个就是突破口
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191101002429730.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQyNDM2MTc2,size_16,color_FFFFFF,t_70)
### 0x03 分析js代码
进入调试器搜索**data-src**, 在 open/static/webpreview/webpreview.js 的第234行追踪到在img内添加属性data-src, 而地址是它的参数, 向上追踪查看是那个地方调用了success函数

![在这里插入图片描述](https://img-blog.csdnimg.cn/20191101002814724.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQyNDM2MTc2,size_16,color_FFFFFF,t_70)
在文件内搜索 **success(**, 定位到status函数, 再次向上追踪, 发现了重要函数ajax, 于是直接进入开发者工具的**网络**查看网络请求, 搜索对应请求
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191101011217724.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQyNDM2MTc2,size_16,color_FFFFFF,t_70)


### 0x04 网络请求
![在这里插入图片描述](https://img-blog.csdnimg.cn/2019110101090930.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQyNDM2MTc2,size_16,color_FFFFFF,t_70)

找到对应**GET**请求:

Request:
```
URL: https://openapi.book118.com/getPreview.html?&project_id=1&aid=178248022&view_token=i_VSDvCjR0Np_Z35o_YIYM1R5rVFWHSO&page=14&callback=jQuery17105378214803355862_1572538572827&_=1572539508883

param:
project_id=1
aid=178248022
view_token=i_VSDvCjR0Np_Z35o_YIYM1R5rVFWHSO
page=14
callback=jQuery17105378214803355862_1572538572827
_=1572539508883
```

Response:

```javascript
jQuery17105378214803355862_1572538572827(
	{
	  "status":200,
	  "message":"ok",
	  "data":{
	    "13":"//view-cache.book118.com/view2/M03/13/2E/wKh2BVyLf5-AEWFWAAHB4yfPcmk260.png",
	    "14":"//view-cache.book118.com/view1/M00/13/25/wKh2BVyLf6KACMtXAAHO9HuAcgY858.png",
	    "15":"//view-cache.book118.com/view3/M01/13/26/wKh2BVyLf6OAE6hqAAHme6fGxJ0634.png",
	    "16":"//view-cache.book118.com/view1/M02/13/25/wKh2BVyLf6GACzc0AAHnZKU_yXM308.png",
	    "17":"//view-cache.book118.com/view2/M04/13/2E/wKh2BVyLf52Ae1WpAAHYX81ZcQ8724.png",
	    "18":"//view-cache.book118.com/view2/M04/13/2E/wKh2BVyLf6KASX_qAAHYvzmhtHs977.png"
	  },
	  "pages":{
	    "preview":"328",
	    "actual":"328"
	  }
	}
	);
```

 分析请求可知

 - page 请求的页面
 - callback 回调函数
 - _ 时间戳

 每次获取会得到后6张图片的地址

 使用postman验证我们的猜想, 尝试获取第100页的图片
 
 ![在这里插入图片描述](https://img-blog.csdnimg.cn/20191101004220300.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQyNDM2MTc2,size_16,color_FFFFFF,t_70)验证成功, 开始编写代码自动进行获取

### 0x05 使用python自动获取地址
思路: 建立一个数据库, 条件循环不断获取6张图片的地址, 直到获取完成. 更改回调函数的名称并使用eval()可以直接执行返回的数据

获取下载地址部分:

main.py
```python
import requests
import time
import sqlite3

total_page = 328  # 已知整本书为328面

db = sqlite3.connect("download.db")
db.execute("""
CREATE TABLE IF NOT EXISTS download(
   page INT PRIMARY KEY,
   url TEXT
);
""")


def get_pages(page):
    def parse(page_data):  # 把callback内容设置为parse, 便可使用eval()函数执行此函数
        for k, v in page_data["data"].items():
            db.execute("INSERT INTO download VALUES (? , ?);", (int(k), "https:" + str(v).replace(r"\/", "/")))
            print("取得页面", k, v)

    url = f"https://openapi.book118.com/getPreview.html?project_id=1&aid=178248022&view_token" \
          f"=i_VSDvCjR0Np_Z35o_YIYM1R5rVFWHSO&page={page}&callback=parse&_={int(time.time()) * 1000} "
    data = requests.get(url=url).text[: -1]  # 最后一个带分号, 需要删除
    eval(data)


def get_max():  # 获取现在应该取哪一个图片
    a = db.execute("""
        SELECT MAX(page) FROM download;
    """)
    for i in a:
        return i[0] + 1 if i[0] else 1


if __name__ == "__main__":
    while (now_page := get_max()) <= total_page:  # 使用了python3.8的海象表达式, 低版本可能会报错
        get_pages(now_page)
        db.commit()
        time.sleep(2)  # 获取过快服务器会拒绝响应, 亲测2秒即可

```
ouput:

![在这里插入图片描述](https://img-blog.csdnimg.cn/20191101005211568.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQyNDM2MTc2,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191101005251356.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQyNDM2MTc2,size_16,color_FFFFFF,t_70)下载图片部分:
download.py

```python
import requests
import sqlite3
import os
from concurrent.futures import ThreadPoolExecutor


def download(page, url):
    try:
        print("下载图片", page, url)
        with open(f"pages/{page}.png", "wb") as f:
            f.write(requests.get(url=url).content)
    except Exception as e:
        print(page, e)


if __name__ == "__main__":
    db = sqlite3.connect("download.db")
    rows = db.execute("SELECT * FROM download;")
    executor = ThreadPoolExecutor(max_workers=10)
    if not os.path.exists("./pages"):
        os.mkdir("./pages")
    for i in rows:
        executor.submit(download, i[0], i[1])
```
 这里我用了线程池, 开了10个线程加快下载速度, 不过我更推荐使用异步来写
 下载成果:
 ![在这里插入图片描述](https://img-blog.csdnimg.cn/20191101010801391.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQyNDM2MTc2,size_16,color_FFFFFF,t_70)至此, 这本书的内容算是下载成功了, 接下来只需要整合成pdf并进行ocr即可, 具体方法不在此赘述
