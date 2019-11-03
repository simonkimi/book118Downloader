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
