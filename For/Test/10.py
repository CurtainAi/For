# 笔趣阁小说下载器
# 2022年7月14日
# 第8次改进
# 主站地址：https://www.bbiquge.net
"""
1、章节信息获取采用多线程 手动同步
2、章节内容获取采用多线程 异步
3、两个自定义函数
4、表格显示
5、清洗数据
"""
import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from urllib import parse
import requests
from lxml import etree
from prettytable import PrettyTable

os.system("mode con cols=160 lines=1125")


def get_HTML(request_link=None):
    request_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62 "
    }
    # 响应数据
    response_data = requests.get(url=request_link, headers=request_header)
    # 断言响应正常
    assert response_data.status_code == 200

    # 尝试多种解码
    try:
        # 获取网页的数据编码
        data_code = requests.utils.get_encodings_from_content(response_data.text)[0]
        # 解码数据
        decrypt_data = response_data.content.decode(data_code)

    except BaseException as e:
        print(e)
        try:
            # 解码数据
            decrypt_data = response_data.content.decode(response_data.apparent_encoding)
        except BaseException as e:
            print(e)
            try:
                # 解码数据
                decrypt_data = response_data.content.decode("utf-8")
            except BaseException as e:
                print(e)
                # 解码数据
                decrypt_data = response_data.text
    # 返回HTML实例
    return etree.HTML(decrypt_data)


def parse_search_data(data=None):
    # 采取搜索的小说
    novel_name = data.xpath('//tr/td[1]/a/text()')
    novel_link = data.xpath('//tr/td[1]/a/@href')
    novel_link = [str(i).split('/')[-2] for i in novel_link]
    latest_chapter = data.xpath('//tr/td[2]/a/text()')
    author = data.xpath('//tr/td[3]/text()')
    total_word = data.xpath('//tr/td[4]/text()')
    update_date = data.xpath('//tr/td[5]/text()')
    # 总字数删除K，除10改为万字
    total_word = [int(int(str(i).replace('K', '')) / 10) for i in total_word]
    # 整合数据
    for i in zip(novel_name, author, total_word, update_date, novel_link, latest_chapter):
        yield list(i)


class novel_downloader:
    def __init__(self):

        # 初始化数据
        self.novels_name = '我有一群地球玩家'  # 需要搜索的小说名
        self.searched_info = []
        self.user_select = None
        self.chapter_info_list = []
        self.start_time = None

    def search_novels(self):
        # 对小说名进行编码
        code_novels_name = parse.quote(self.novels_name, encoding='gbk')
        # 补全链接
        novel_link = f'https://www.bbiquge.net/modules/article/search.php?' \
                     f'searchtype=articlename&searchkey={code_novels_name}&page=1'
        # 获取待解析数据
        need_parsed_data = get_HTML(request_link=novel_link)
        # 获取页列表
        page_list = need_parsed_data.xpath('//*[@class="pagelink"]/em/text()')

        if len(page_list) != 0:
            # 获取最大页数
            max_page = str(page_list[0]).split('/')[1]
            # 最大页不为1时
            if max_page != 1:
                for page in range(1, int(max_page) + 1):
                    # 补全页链接
                    page_link = f'https://www.bbiquge.net/modules/article/search.php?' \
                                f'searchtype=articlename&searchkey={code_novels_name}&page={page}'
                    # 获取待解析数据
                    need_parsed_data = get_HTML(request_link=page_link)
                    # 添加到搜索信息列表
                    self.searched_info += parse_search_data(data=need_parsed_data)

        else:
            # 没有搜索到或者重定向了 先看是否重定向了
            author_list = need_parsed_data.xpath('//h1//a/text()')
            if len(author_list) != 0:  # 被重定向了
                # 获取作者名
                author = author_list[0]
                # 编码作者名
                code_author = parse.quote(author, encoding='gbk')
                # 补全作者链接
                author_link = f'https://www.bbiquge.net/modules/article/authorarticle.php?author={code_author}'
                # 获取待解析数据
                need_parsed_data = get_HTML(request_link=author_link)
                # 添加到搜索信息列表，调用自定义解析函数
                self.searched_info += parse_search_data(data=need_parsed_data)
            else:
                input('没有搜索到：，任意键启用默认')
                self.novels_name = '我有一群地球玩家'
                self.search_novels()
                return

    def print_novel_info(self):
        # 对搜索到的数据根据字数升序
        self.searched_info.sort(key=lambda x: x[2])
        # 插入ID号
        for a in range(len(self.searched_info)):
            self.searched_info[a].insert(0, a)

        os.system('cls')
        table = PrettyTable()
        table.field_names = ["编号", "小说名", "作者", "万字", "更新日期", '链接', "最新章节", ]
        table.align['小说名'] = 'l'
        table.align['最新章节'] = 'l'
        table.align['作者'] = 'l'
        table.align['最新章节'] = 'l'
        table.align['万字'] = 'l'
        table.align['更新日期'] = 'l'
        table.add_rows(self.searched_info)
        print(table.get_string(title=self.novels_name))

    def select_novel(self):
        print('输入书名重新搜索，或者输入编号选择书籍')
        select = input(f'编号 0-{len(self.searched_info) - 1}：')  # 用户输入接口
        if select.isdigit():  # 检查用户输入是否位数字
            select = int(select)
            if 0 <= select < len(self.searched_info):  # 检查输入范围
                print(self.searched_info[select])
                if input('确认选中(Y/N)').upper() == 'Y':
                    self.user_select = self.searched_info[select]
                else:
                    self.select_novel()
            else:
                self.select_novel()  # 不在范围内重新调用选择菜单
        else:
            self.searched_info = []  # 清空列表
            self.novels_name = select  # 复写书名
            self.search_novels()
            self.print_novel_info()
            self.select_novel()
            return

    def multi_thread_task_get_chapter_info(self, page):
        # 补全页链接
        page_lins = f'https://www.bbiquge.net/book/{self.user_select[-2]}/index_{page}.html'
        # 调用自定义函数
        need_parsed_data = get_HTML(request_link=page_lins)
        # 解析章节信息
        chapter_name = need_parsed_data.xpath('//dl/dd/a/text()')
        chapter_lins = need_parsed_data.xpath('//dl/dd/a/@href')
        # 添加到章节信息列表，这是手动同步的关键，不然章节顺序会打乱
        self.chapter_info_list.append([page, chapter_name, chapter_lins])

    def get_chapter_info(self):
        # 开始时间
        self.start_time = time.time()
        print('正在采集章节信息，需要十多秒')
        # 小说链接
        novel_link = f'https://www.bbiquge.net/book/{self.user_select[-2]}/'
        need_parsed_data = get_HTML(request_link=novel_link)
        page_list = need_parsed_data.xpath('//option/text()')
        max_page = len(page_list)
        if max_page != 0:
            # 线程池
            pool = ThreadPoolExecutor(max_workers=max_page)  # 线程不蹦我不蹦
            # 任务池
            all_task = [pool.submit(self.multi_thread_task_get_chapter_info, page) for page in range(1, max_page + 1)]
            wait(all_task, return_when=ALL_COMPLETED)
            pool.shutdown()  # 关闭线程池

        # 这里手动把异步多线程产生的数据同步了，
        # 排序，手动同步章节信息，
        self.chapter_info_list.sort(key=lambda x: x[0])
        # 整理章节信息，格式：章节名，章节链接
        self.chapter_info_list = [list(b) for a in self.chapter_info_list for b in zip(a[1], a[2])]
        # 插入ID，格式：ID,章节名，章节链接
        for i in range(len(self.chapter_info_list)):
            self.chapter_info_list[i].insert(0, i)

    def multi_thread_task_get_chapter_content(self, i):
        # 章节文件路径
        chapter_path = f'./笔趣阁/{self.user_select[1]}/{i}.txt'
        # 章节链接
        chapter_link = f'https://www.bbiquge.net/book/{self.user_select[5]}/{self.chapter_info_list[i][2]}'
        # 文件存在了，就退出任务
        if os.path.isfile(chapter_path):
            print(f'跳过：{self.chapter_info_list[i][1]}')
            return
        else:
            # 下载保存章节内容
            print(f'下载：{self.chapter_info_list[i][1]}')
            need_parsed_data = get_HTML(request_link=chapter_link)
            chapter_content = need_parsed_data.xpath('//div[@id="content"]//text()')
            with open(file=chapter_path, mode='a', encoding='utf-8') as w:
                for i in chapter_content:
                    w.write(i)
                    w.write('\n')

    def get_chapter_content(self):
        # 主要目录不存在就创建
        main_dir = f'./笔趣阁/{self.user_select[1]}/'
        if not os.path.isdir(main_dir):
            os.makedirs(main_dir)
        # 线程池
        pool = ThreadPoolExecutor(max_workers=1000)  # 线程不蹦我不蹦
        # 任务池
        all_task = [pool.submit(self.multi_thread_task_get_chapter_content, i) for i in
                    range(len(self.chapter_info_list))]
        wait(all_task, return_when=ALL_COMPLETED)

    def arrange_data(self):
        # 小说文件存在就删除
        novel_file_path = f'./笔趣阁/{self.user_select[1]}.txt'
        if os.path.isfile(novel_file_path):
            os.remove(novel_file_path)
        # 打开小说文件
        with open(file=f'./笔趣阁/{self.user_select[1]}.txt', mode='a', encoding='utf-8') as w:
            # 展开章节信息，根据ID顺序读取章节文件写入小说文件
            for a in self.chapter_info_list:
                # 章节文件位置，不存在就回去下载了再过来
                chapter_file_path = f'./笔趣阁/{self.user_select[1]}/{a[0]}.txt'
                if not os.path.isfile(chapter_file_path):
                    self.get_chapter_content()
                # 读取章节内容文件
                with open(file=chapter_file_path, mode='r', encoding='utf-8') as r:
                    w.write(a[1])
                    w.write('\n')
                    data = r.readlines()
                    # 清洗一些不要的
                    data = data[3:]
                    data = [str(i).replace(' ', '') for i in data]
                    data = [i for i in data if i != '']
                    data = [str(i).replace(r'\r', '') for i in data]
                    data = [str(i).replace(r'\n', '') for i in data]
                    data = json.dumps(data, ensure_ascii=False)
                    data = data.replace('\\r', '')
                    data = data.replace('\\n', '')
                    data = data.replace(' ', '')
                    data = data.replace('\u3000', '')
                    data = json.loads(data)
                    # 检查内容是否和章节重复
                    if re.findall(r"第(.+?)章", a[1]) == re.findall(r"第(.+?)章", data[0]):
                        data.remove(data[0])
                    for b in data:
                        w.write(b)
                        w.write('\n')
        print("下载总共用时{}秒".format((time.time() - self.start_time)))

    def start_main(self):
        self.search_novels()
        self.print_novel_info()
        self.select_novel()
        self.get_chapter_info()
        self.get_chapter_content()
        self.arrange_data()
        return


if __name__ == '__main__':
    down = novel_downloader()
    while True:
        down.start_main()