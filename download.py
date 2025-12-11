#!/usr/bin/env python3
# download.py
import os, requests
from concurrent.futures import ThreadPoolExecutor   # 轻量级并发
from functools import partial

def download(url, save_dir='images'):
    os.makedirs(save_dir, exist_ok=True)
    name = os.path.basename(url) or f'img_{abs(hash(url))}.jpg'
    path = os.path.join(save_dir, name)
    try:
        r = requests.get(url, stream=True, timeout=10,
                         headers={'User-Agent':'Mozilla/5.0'})
        r.raise_for_status()
        with open(path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        print('ok:', path)
    except Exception as e:
        print('fail:', url, e)


img_args = [
    {"url_pre": "https://abook.hep.com.cn/ICourseFiles/5000004114/swfresourses/2021/4/3/1617389209482/1617389209482.files/", "num": 4},
    {"url_pre": "https://abook.hep.com.cn/ICourseFiles/5000004114/swfresourses/2021/4/3/1617389311270/1617389311270.files/", "num": 9},
    {"url_pre": "https://abook.hep.com.cn/ICourseFiles/5000004114/swfresourses/2021/4/3/1617389386989/1617389386989.files/", "num": 8},
    {"url_pre": "https://abook.hep.com.cn/ICourseFiles/5000004114/swfresourses/2021/4/3/1617389462728/1617389462728.files/", "num": 7},
    {"url_pre": "https://abook.hep.com.cn/ICourseFiles/5000004114/swfresourses/2021/4/3/1617389550388/1617389550388.files/", "num": 7},
    {"url_pre": "https://abook.hep.com.cn/ICourseFiles/5000004114/swfresourses/2021/4/3/1617389649901/1617389649901.files/", "num": 31},
]

with ThreadPoolExecutor(max_workers=8) as pool:
    for index, img_arg in enumerate(img_args):
        url_list = [f"{img_arg["url_pre"]}{i+1}.png" for i in range(img_arg["num"])]
        pool.map(partial(download, save_dir=f"img/{index + 1}"), url_list)
