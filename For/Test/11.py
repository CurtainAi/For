import linecache
import os
import re
from faker import Faker
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter
from tqdm import tqdm
import requests
import sqlite3
import urllib.parse


def creat_table(table_name):
    conn = sqlite3.connect('douyin.db')
    c = conn.cursor()
    c.execute(f'''CREATE TABLE IF NOT EXISTS t_{table_name}
           (ID INTEGER PRIMARY KEY AUTOINCREMENT,VID TEXT NOT NULL);''')
    conn.commit()
    conn.close()


def insert_data(table_name, vid):
    conn = sqlite3.connect('douyin.db')
    c = conn.cursor()
    cursor = c.execute(f"SELECT vid from t_{table_name}")
    already_have = False
    for row in cursor:
        if vid in row:
            already_have = True
    if already_have is False:
        c.execute(f"INSERT INTO t_{table_name} (ID,VID) VALUES (null,{vid})")
    conn.commit()
    conn.close()


def selet_data(table_name):
    conn = sqlite3.connect('douyin.db')
    c = conn.cursor()
    cursor = c.execute(f"SELECT VID from t_{table_name}")
    vid_list = [out_exp[0] for out_exp in cursor]
    return vid_list


class Douyin:
    def __init__(self, url):
        self.share_url = url
        self.headers = {
            'User-Agent': "Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1C28 Safari/419.3"
        }
        self.sec_uid = None
        self.uid = None
        self.nick_name = None

    def get_user_info(self):
        resp = requests.get(self.share_url, headers=self.headers)
        self.sec_uid = 'sec_uid=' + urllib.parse.parse_qs(urllib.parse.urlparse(resp.url).query)['sec_uid'][0]
        user_info = f'https://www.iesdouyin.com/web/api/v2/user/info/?{self.sec_uid}'
        resp = requests.get(user_info, headers=self.headers)
        user_data = {
            'signature': resp.json()['user_info']['signature'],
            'nickname': resp.json()['user_info']['nickname'],
            'aweme_count': resp.json()['user_info']['aweme_count'],
            'following_count': resp.json()['user_info']['following_count'],
            'total_favorited': resp.json()['user_info']['total_favorited'],
            'avatar': resp.json()['user_info']['avatar_larger']['url_list'][0],
        }
        self.uid = resp.json()['user_info']['uid']
        self.nick_name = re.sub(r'[<|>\/:"*?]', '_', resp.json()['user_info']['nickname'])
        creat_table(self.uid)
        return user_data

    def get_all_video(self):
        max_cursor = 0
        video_has_more = True
        all_video_list = []
        if self.sec_uid is None:
            self.get_user_info()
        while video_has_more is True:
            json_url = f'https://www.iesdouyin.com/web/api/v2/aweme/post/?{self.sec_uid}&' \
                       f'count=21&max_cursor={max_cursor}'
            resp = requests.get(json_url, headers=self.headers)
            video_has_more = resp.json()['has_more']
            max_cursor = resp.json()['max_cursor']
            video_list = resp.json()['aweme_list']
            for i in video_list:
                try:
                    all_video_list.append({'desc': i['desc'], 'vid': i['video']['vid'], 'aweme_id': i['aweme_id']})
                except KeyError:
                    all_video_list.append({'desc': i['desc'], 'vid': None, 'aweme_id': i['aweme_id']})
        print(all_video_list)
        return all_video_list

    def down_video(self, down_info, index):
        alreday_down = False
        retry = 0
        session = requests.session()
        session.mount('https://', HTTPAdapter(max_retries=5))
        alreday_down_video = selet_data(self.uid)
        for n in alreday_down_video:
            if down_info['aweme_id'] in n:
                alreday_down = True
                break
        if alreday_down is False:
            if os.path.exists(self.nick_name) is False:
                try:
                    os.makedirs(self.nick_name)
                except FileExistsError:
                    pass
            if down_info['desc'] == '':
                down_info['desc'] = down_info['aweme_id']
            down_info['desc'] = re.sub(r'[<|>\/:"*?\n]', '_', down_info['desc'])
            save_name = f'{self.nick_name}/{index.zfill(2)}_{down_info["desc"]}.mp4'
            if down_info["vid"]:
                download_url = f'https://aweme.snssdk.com/aweme/v1/play/?video_id={down_info["vid"]}&ratio=1080p'
                response = session.get(download_url, headers=self.headers, stream=True)
                while response.content == b'' and retry < 3:
                    self.headers = {
                        'User-Agent': Faker().chrome()
                    }
                    response = session.get(download_url, headers=self.headers)
                    retry += 1
                if response.content:
                    with open(save_name, 'wb') as file:
                        file.write(response.content)
                    insert_data(self.uid, down_info['aweme_id'])
                else:
                    with open(f'{self.nick_name}/下载失败视频.txt', 'a+') as file:
                        file.write(download_url + '\n')
            else:
                n = 0
                img_json_url = f'https://www.douyin.com/web/api/v2/aweme/iteminfo/?item_ids={down_info["aweme_id"]}'
                if os.path.exists(f'{self.nick_name}/{down_info["desc"]}') is False:
                    try:
                        os.makedirs(f'{self.nick_name}/{down_info["desc"]}')
                    except FileExistsError:
                        pass
                response = session.get(img_json_url, headers=self.headers)
                for i in response.json()["item_list"][0]["images"]:
                    n += 1
                    img_url = i["url_list"][0]
                    img_content = session.get(img_url, headers=self.headers).content
                    img_save_name = f'{self.nick_name}/{down_info["desc"]}/{n}.jpg'
                    with open(img_save_name, 'wb') as file:
                        file.write(img_content)


def main(share_url, down_all=False):
    share_url = re.search(r'[a-zA-z]+://[^\s]*', share_url).group()
    douyin = Douyin(share_url)

    info = douyin.get_user_info()
    #print(info)
    print(f'作者:{info["nickname"]}\n视频数:{info["aweme_count"]}\n{"-" * 20}\n拉取作者所有作品中...')
    down_list = douyin.get_all_video()
    print(down_list)
    down_mode = '1'
    if not down_all:
        down_mode = input(f'{"-" * 20}\n选择下载模式:\n1.全部下载\n2.关键词匹配下载\n')

    def down_task(down_load):
        with ThreadPoolExecutor(max_workers=10) as t:
            obj_list = []
            for i in range((len(down_load))):
                obj = t.submit(douyin.down_video, down_load[i], str(i))
                obj_list.append(obj)
            with tqdm(total=len(down_load), ncols=100) as bar:
                for x in as_completed(obj_list):
                    bar.update(1)

    if down_mode == '1':
        if down_list:
            down_task(down_list)

        else:
            print(f'无视频可下载')
    elif down_mode == '2':
        k = 0
        filter_down_list = []
        keyword = input('请输入关键词:')
        for v in down_list:
            if keyword in v['desc']:
                filter_down_list.append(v)
        if len(filter_down_list) == 0:
            print('无匹配记录')
        else:
            print(f'共找到 {len(filter_down_list)} 条匹配记录, 开始下载')
            print(filter_down_list)
            down_task(filter_down_list)
    else:
        print('输入错误')


if __name__ == '__main__':
    main('4- 长按复制此条消息，打开抖音搜索，查看TA的更多作品。 https://v.douyin.com/MHfxNQd/')
    # share_url_list = linecache.getlines('D:\作者主页链接.txt',)
    # # linecache.clearcache()
    #
    # if share_url_list:
    #     print('已检测到有批量下载文件,进入批量下载模式\n')
    #     if input('请选择批量下载模式:\n1.下载所有作者所有视频\n2.手动选择每个作者下载模式\n') == '1':
    #         down_all = True
    #     else:
    #         down_all = False
    #     for i in share_url_list:
    #         main(i, down_all)
    #         print(f'当前任务完成\n{"*" * 30}\n')
    #     input('所有任务已完成')
    # else:
    #     url = input('输入作者主页分享链接:')
    #     main(url)
    #     input('任务已完成')