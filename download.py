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

