import os
import time
import re
from lxml import etree
import requests
from selenium import webdriver
import json

regular_video_ids = 'video_id=(.*?)&'
# regular_username = '"name": "(.*?)",'
# regular_url = 'a href="(.*?)">Found</a>'

# 定义函数get_video_ids(author_url),返回UP主全部短视频的ID的列表
# 参数author_url:抖音UP主的主页
# 例如，XXX的主页 https://www.douyin.com/user/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
def get_video_ids(author_url):
    ids = list()
    count = 0
    retry = 0
    n = 0
    flag = True
    chrome_option = webdriver.ChromeOptions()
    #chrome_option.add_argument('headless')  # 静默模式
    driver = webdriver.Chrome(options=chrome_option)
    driver.get(author_url)
    while flag and retry <= 15:
        driver.execute_script("window.scrollBy(0,2000)")  # scrollBy(x, y)，JavaScript中操作内容滚动指定的像素数
        n = n + 1
        time.sleep(2)
        html_source = driver.page_source
        items = etree.HTML(html_source).xpath("//li[@class='ECMy_Zdt']")
        count_items = len(items)
        print("操作页面内容滚动{0:0>3}次后,获取视频ID{1:0>4}个。".format(n, count_items))
        if count_items != count:
            count = count_items
        else:
            if retry < 15:
                retry = retry + 1
            else:
                flag = False
                print("已经达到可获取视频ID的最大数量,开始逐个获取视频ID:\n")
                for item in items:
                    video_id = item.xpath("a/@href")[0].split("/")[-1]
                    print("获取短视频ID:{}".format(video_id))
                    ids.append(video_id)
    print(ids)
    return ids


# 定义函数get_video_info(video_id),返回元组(短视频下载地址,短视频标题)
# 参数video_id:抖音短视频唯一ID
def get_video_info(video_id):
    # 通过url0获取json数据(Chrome浏览器，F12进入开发者模式，模拟手机端，可以看到url0)
    url0 = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=" + video_id
    r_url0 = requests.get(url0, headers={"user-agent": "Mozilla/5.0"})
    # 获取json数据中的视频地址及视频标题
    # 出现错误！
    url1 = r_url0.json()["item_list"][0]['video']["play_addr"]["url_list"][0]
    # 防止出现空标题，加上短视频ID
    title = video_id + "-" + r_url0.json()["item_list"][0]['share_info']["share_title"].split("#")[0].split("@")[0]
    # 获取url1重定向后的真实视频地址
    r_url1 = requests.get(url1, headers={"user-agent": "Mozilla/5.0"}, allow_redirects=False)
    url = r_url1.headers['Location']
    return url, title

# 获取无码视频
def get_video_info2(video_id):
    # www.douyin.com/video/7089747820005035305
    # 通过url0获取json数据(Chrome浏览器，F12进入开发者模式，模拟手机端，可以看到url0)
    url_json = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=" + video_id
    print(url_json)
    r_url_json = requests.get(url_json, headers={"user-agent": "Mozilla/5.0"})
    print(r_url_json.text)
    # 获取json数据中的视频地址及视频标题
    # 出现错误！
    try:
        url_video_id = r_url_json.json()['item_list'][0]['video']['play_addr']['url_list'][0]
        video_ids = re.findall(regular_video_ids,url_video_id)[0]
        url_video_ids='https://aweme.snssdk.com/aweme/v1/play/?video_id={}&line=0&ratio=540p&media_type=4&vr_type=0&improve_bitrate=0&is_play_url=1&is_support_h265=0&source=PackSourceEnum_PUBLISH'.format(video_ids)
        # 防止出现空标题，加上短视频ID
        title = video_id + "-" + r_url_json.json()["item_list"][0]['share_info']["share_title"].split("#")[0].split("@")[0]
        # # 获取url1重定向后的真实视频地址
        # r_url1 = requests.get(url1, headers={"user-agent": "Mozilla/5.0"}, allow_redirects=False)
        # url = r_url1.headers['Location']
    except:
        url_video_ids = r_url_json.json()['item_list'][0]['image_infos'][0]['label_large']['url_list'][3]
        # url_video_ids='https://aweme.snssdk.com/aweme/v1/play/?video_id={}&line=0&ratio=540p&media_type=4&vr_type=0&improve_bitrate=0&is_play_url=1&is_support_h265=0&source=PackSourceEnum_PUBLISH'.format(video_ids)
        # 防止出现空标题，加上短视频ID
        title = video_id + "-" + r_url_json.json()["item_list"][0]['share_info']["share_title"].split("#")[0].split("@")[0]
        # # 获取url1重定向后的真实视频地址
        # r_url1 = requests.get(url1, headers={"user-agent": "Mozilla/5.0"}, allow_redirects=False)
        # url = r_url1.headers['Location']

    return url_video_ids, title


# 定义函数get_file_name(string),从字符串中提取合法文件名
def get_file_name(string):
    pattern = re.compile(r'[?*/\\|.:><]')
    txt = re.sub(pattern, '', string)
    return txt


# 定义函数download_video(save_path, url, title),下载并以短视频标题作为文件名保存短视频到指定路径
def download_video(save_path, url, title):
    if os.path.exists(save_path):
        pass
    else:
        os.makedirs(save_path)
    with requests.get(url, headers={"user-agent": "Mozilla/5.0"}, stream=True) as r:
        total_size = int(int(r.headers["Content-Length"]) / 1024 + 0.5)
        file_name = get_file_name(title)
        full_path = save_path + get_file_name(title) + ".mp4"
        with open(file=full_path, mode="wb") as f:
            time.sleep(2)
            print('当前下载:【{}】,视频文件大小:【{}KB】'.format(file_name, total_size))
            count = 0
            scale = 50
            start = time.perf_counter()
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
                count = count + 1
                i = int(scale * (count / total_size))
                a = "=" * i
                b = "." * (scale - i)
                c = (i / scale) * 100
                dur = time.perf_counter() - start
                speed = count / dur
                print("\r下载进度:{0:^3.0f}%[{1:}>{2:}] 耗时:{3:.2f}s 平均下载速度:{4:.2f}KB/S。".format(c, a, b, dur, speed),end="")
            print("\n视频文件下载完毕,存放于:【{0:}】。".format(full_path))

def get_username(url):
    headers = {
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    }
    shroturl = re.findall('[a-z]+://[\S]+', url, re.I | re.M)[0]
    startpage = requests.get(url=shroturl, headers=headers, allow_redirects=False)
    location = startpage.headers['location']
    sec_uid = re.findall('(?<=sec_uid=)[a-z，A-Z，0-9, _, -]+', location, re.M | re.I)[0]
    getname = requests.get(url='https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid={}'.format(sec_uid),headers=headers).text
    userinfo = json.loads(getname)
    name = userinfo['user_info']['nickname']
    name = get_file_name(name)
    return name


# 定义主程序
def main():
    # 获取UP主全部短视频的ID
    url = input("请输入抖音UP主的主页:")
    print("\n获取UP主全部短视频的ID...")
    # https://v.douyin.com/FPFQ2LA/
    # https://v.douyin.com/FPhVyN9/
    # url = 'https://v.douyin.com/FPhVyN9/'
    username =get_username(url)
    print("用户名称【{}】".format(username))
    ids = get_video_ids(url)
    # ids= ['7001698434696645903', '6637050534777851150', '6549263545836506371', '7038867576688102664', '7035185621438041374', '7033753691391888677', '7032252014436338975', '7030738963782487309', '7028882926003571976', '7027301594836258056', '7026281927854296357', '7024741081694670110', '7023595146742713613', '7022517071678295326', '7022130359919856910', '7020719491906637090', '7019534809810668835', '7018510751933467904', '7017278774026734863', '7016158178224131362', '7011717865623588136', '7010236707043822863', '7009123816890830080', '7007754583241952527', '7006586177465748771', '7005503348543638818', '7003984905847852329', '7003288911686536489', '7000213331638291727', '6998781092777954594', '6998363374232849679', '6998108413972581666', '6996254730238414115', '6995883383687499023', '6991798279994412323', '6836274978170670336', '6835159425460800783', '6804042321563372800', '6801829227923574016', '6799615694574144783', '6795538064560213248', '6794021394712628480', '6793321615238221056', '6754633591256288516', '6706731597808356621', '6705160739197406472', '6692327428691397900', '6687027214296435982', '6660799388555775245', '6657760440900193543', '6654357735833963779', '6653764039421758732', '6653702649143168260', '6652311341434457347', '6651516530896997635', '6650993780520520974', '6650018005176618248', '6649631259578469646', '6649300953805622541', '6647065408186617101', '6645833029639998734', '6644837081946262797', '6644478064447196423', '6644104800277368078', '6643742655966612749', '6643271616857902349', '6642867404311366925', '6642627086294977806', '6641121201152331012', '6640757064278740227', '6640413393016605956', '6639512175452884238', '6639461884200226056', '6638503353317854467', '6638159368871234820', '6634074302209592590', '6632592080810020100', '6632221093115464973', '6631485467453820168', '6628890222388055303', '6627370731472686339', '6627035665412394254', '6626686119146687757', '6624829655738223876', '6624457029203266824', '6619990295561899272', '6619614360786455821', '6618858399792631047', '6618476483016920327', '6615925135050280195', '6605427763711053059', '6600245114549832964', '6597333593305910531', '6596609801168358669', '6596098901063765252', '6588442150311038216', '6583274468188097796', '6578442407208029448', '6575495101634579716', '6573985256498531597', '6562009307011878147', '6561591960610540807', '6561029749349551368', '6558947943657770247', '6558583743580212494', '6557881073173269764', '6557666011347160323', '6557506468843621646', '6556712342766226692', '6556416222068477197', '6555879926036172036', '6555609446876187917', '6555586302635412750', '6555229459048303879', '6554128133245635853', '6553769409003916557', '6553433563419643140', '6553234238156573960', '6553074281234828547', '6552911599470906637', '6552651049088322830', '6552630695141838088', '6552567663405567235', '6552301962598026504', '6552300518075534600', '6551881371931905293', '6551525808765144324', '6549251957461110024', '6548031918649117959', '6547698205763570958', '6547488378286247182', '6547395023044873485', '6544944037944626435', '6544494695433637127', '6543832581433986312', '6542339335880969480', '6542302058748316942', '6538884592605072644', '6538260456560135437', '6535907487579639044', '6535519212079680782', '6535135596879285508']
    # ids = ['6557881073173269764', '6557666011347160323', '6557506468843621646', '6556712342766226692', '6556416222068477197', '6555879926036172036', '6555609446876187917', '6555586302635412750', '6555229459048303879', '6554128133245635853', '6553769409003916557', '6553433563419643140', '6553234238156573960', '6553074281234828547', '6552911599470906637', '6552651049088322830', '6552630695141838088', '6552567663405567235', '6552301962598026504', '6552300518075534600', '6551881371931905293', '6551525808765144324', '6549251957461110024', '6548031918649117959', '6547698205763570958', '6547488378286247182', '6547395023044873485', '6544944037944626435', '6544494695433637127', '6543832581433986312', '6542339335880969480', '6542302058748316942', '6538884592605072644', '6538260456560135437', '6535907487579639044', '6535519212079680782', '6535135596879285508']
    print("获取完毕!共获取短视频ID{}个!".format(len(ids)))
    # 根据短视频ID,批量获取下载地址、短视频标题
    print("\n根据短视频的ID获取短视频的下载地址、标题信息...")
    videos_info = list()
    # www.douyin.com/video/7089747820005035305
    # 出现错误！
    for video_id in ids:
        video_info = get_video_info2(video_id)
        videos_info.append(video_info)
        print("短视频标题:【{0:}】;下载地址:【{1:}】".format(video_info[1], video_info[0]))

    # 批量下载短视频
    print("\n开始批量下载短视频:")
    # 自定义下载目录
    # 返回当前目录
    #cwd = os.getcwd(r"D:\00 DownLoad\DouyinDownload")
    path = r"D:\00 DownLoad\DouyinDownload"
    path = path + "/{}/".format(username)
    print(path)
    total = len(videos_info)
    for i in range(total):
        print("\n将下载第【{0:0>4}/{1:0>4}】个短视频:".format(i + 1, total))
        print("=" * 50)
        download_video(path, videos_info[i][0], videos_info[i][1])


if __name__ == "__main__":
    # get_video_info2("7089747820005035305")
    main()