# -*- coding: utf-8 -*-
# date：2021/12/13
import json
import requests
import time
import random


class bili_exp:
    """
    登录bilibili网页，浏览器按F12-网络，刷新浏览器在开发者工具里找cookie复制
    """

    def __init__(self, c, coin_operated=None):
        self.cookie = c if type(c) == dict else self.extract_cookies(c)
        self.coin_operated = coin_operated
        self.s = requests.Session()
        self.headers = {"Content-Type": "application/x-www-form-urlencoded",
                        "Connection": "keep-alive",
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4728.0 Safari/537.36 Edg/98.0.1093.6'}
        self.csrf = self.cookie['bili_jct']

    @staticmethod
    def extract_cookies(cookies):
        cookies = dict([i.split("=", 1) for i in cookies.split("; ")])
        return cookies

    def getCoin(self):
        """
        获取硬币数量
        """
        url = "http://account.bilibili.com/site/getCoin"
        res = self.s.get(url, cookies=self.cookie, headers=self.headers).json()
        money = res['data']['money']
        return int(money)

    def getInfo(self):
        url = "http://api.bilibili.com/x/space/myinfo"
        data = self.s.get(url, cookies=self.cookie, headers=self.headers).json()['data']
        global username
        username = data['name']
        global uid
        uid = data['mid']
        level = data['level']
        current_exp = data['level_exp']['current_exp']
        next_exp = data['level_exp']['next_exp']
        require_exp = int(next_exp) - int(current_exp)
        if self.coin_operated:
            days = int(int(require_exp) / 65)
        else:
            days = int(int(require_exp) / 15)
        coin = self.getCoin()
        msg = f"欢迎 {username}！当前等级：{level}，当前经验：{current_exp}，还需{require_exp}经验升级，需要{days}天，当前硬币数量：{coin}\n"
        return current_exp, msg

    def getvideo(self):
        uids = ['473837611', '20165629', '649022917', '612492134']
        # 分别是 新华社，共青团中央，火星方阵，司马南的UID，可在关注的up空间右下角找到，替换或添加到列表即可
        url = f'https://api.bilibili.com/x/space/arc/search?mid={random.choice(uids)}'
        res = self.s.get(url, headers=self.headers).json()['data']['list']['vlist']
        return res

    def viewvideo(self, bvid):
        playedTime = random.randint(10, 100)
        url = "https://api.bilibili.com/x/click-interface/web/heartbeat"
        data = {
            'bvid': bvid,
            'played_time': playedTime,
            'csrf': self.csrf
        }
        j = self.s.post(url, data=data).json()
        code = j['code']
        if code == 0:
            print('看视频完成!')
        else:
            print('看视频失败!')

    def sharevideo(self, bvid):
        url = "https://api.bilibili.com/x/web-interface/share/add"
        data = {
            'bvid': bvid,
            'csrf': self.csrf
        }
        res = self.s.post(url, data=data, cookies=self.cookie, headers=self.headers).json()
        code = res['code']
        if code == 0:
            print('分享成功!')
        else:
            print('分享失败!')

    def toubi(self, bvid):  # 投币
        coinNum = self.getCoin()
        if coinNum == 0:
            print('太穷了，硬币不够!')
            return -99
        url = "http://api.bilibili.com/x/web-interface/coin/add"
        data = {
            'bvid': bvid,
            'multiply': 1,
            'select_like': 1,
            'csrf': self.csrf
        }
        res = self.s.post(url, data=data, cookies=self.cookie).json()
        code = res['code']
        if code == 0:
            print(bvid + ' 投币成功!')
            return 1
        else:
            print(bvid + ' 投币失败!')
            return 0

    def task(self):
        coin_num = self.getCoin()
        k = 0
        for i in range(10):
            vlist = self.getvideo()
            random_list = random.randint(0, len(vlist) - 1)
            bvid = vlist[random_list]['bvid']
            title = vlist[random_list]['title']
            up = vlist[random_list]['author']
            print('-' * 30 + f'\n正在观看视频 {i + 1}. {bvid} - {title} - {up}')
            self.viewvideo(bvid)
            time.sleep(1)
            self.sharevideo(bvid)
            time.sleep(1)
            if self.coin_operated and coin_num:
                while k < min(coin_num, 5):
                    coin_code = self.toubi(bvid)
                    time.sleep(1)
                    if coin_code == 1:
                        k += 1
                        coin_num -= 1
                        break

    def start(self):
        exp1, msg = self.getInfo()
        print(msg)
        print(f'{username}：')
        self.task()
        exp2, a = self.getInfo()
        print('-' * 30 + f'\n任务完成，获得经验{int(exp2) - int(exp1)}\n' + '-' * 30 + '\n')


def main():
    #cookie = 'Cookie: innersign=0; buvid3=8DCC9651-F482-33EF-53AA-45F84C46696163895infoc; b_lsid=D3853B96_17DD548E719; _uuid=21019EC32-FB108-35CD-DDB5-2F69E246638664552infoc; buvid_fp=8DCC9651-F482-33EF-53AA-45F84C46696163895infoc; fingerprint=1e92d010bf50e31f39e16a1cbf7bc5e8; buvid_fp_plain=DB455660-E133-2FA6-0C8B-E1523939BBE622958infoc; SESSDATA=08386596%2C1655512892%2Cc8b22%2Ac1; bili_jct=ae672b9240d30bddb264dfaa119bd4a8; DedeUserID=2895820; DedeUserID__ckMd5=b8aa393a6f0353f0; sid=c9lzvsmp; i-wanna-go-back=1; b_ut=6'  # 浏览器开发者工具复制cookie,支持多账号，cookie之间用&连接
    cookie = 'Cookie: innersign=0; buvid3=8DCC9651-F482-33EF-53AA-45F84C46696163895infoc; b_lsid=D3853B96_17DD548E719; _uuid=21019EC32-FB108-35CD-DDB5-2F69E246638664552infoc; buvid_fp=8DCC9651-F482-33EF-53AA-45F84C46696163895infoc; fingerprint=1e92d010bf50e31f39e16a1cbf7bc5e8; buvid_fp_plain=DB455660-E133-2FA6-0C8B-E1523939BBE622958infoc; SESSDATA=c2503a78%2C1667785526%2Ccf42b%2A51; bili_jct=aaf4a6cd4d04b279ba9609805713c310; DedeUserID=2895820; DedeUserID__ckMd5=b8aa393a6f0353f0; sid=c9lzvsmp; i-wanna-go-back=1; b_ut=6'  # 浏览器开发者工具复制cookie,支持多账号，cookie之间用&连接

    # cookie = {
    #     "Userid":"2895820",
    #     "SessData":"c2503a78%2C1667785526%2Ccf42b%2A51",
    #     "BiliJct":"aaf4a6cd4d04b279ba9609805713c310",
    # }

    for c in cookie.split('&'):
        b = bili_exp(c)  # 不投币取消本行注释，并注释下一行
        # b = bili_exp(c, 1)  # 投币需注释上一行，并取消本行注释
        b.start()


def main_handler(*args):  # 腾讯云函数
    main()


def handler(*args):  # 阿里云函数
    main()


if __name__ == '__main__':
    main()