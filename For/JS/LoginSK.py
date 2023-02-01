import requests


headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "http://login.shikee.com",
    "Referer": "http://login.shikee.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}
cookies = {
    "Hm_lvt_f5b004b0742ab157215b881269b4a6fa": "1673847375",
    "ci_session": "a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22154fb0a4e8444bcd502d3a79d7b800aa%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A15%3A%22123.235.148.143%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A111%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F109.0.0.0+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1673847378%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7D8fb0b254e5faec40875fc88853247e06",
    "Hm_lpvt_f5b004b0742ab157215b881269b4a6fa": "1673847380",
    "PHPSESSID": "82qip98m683rq4hbki26jvaht4",
    "shikeeName": "%u4F60%u5728%u54EA%u91CC%u5440"
}
url = "http://login.shikee.com/check/"
params = {
    "": "",
    "_1673848425825": ""
}
data = {
    "username": "你在哪里呀",
    "password": "3c09e60e3b6874a4cda52de5123081bed1e60973c0f704e0dbbe76044c78606617ee0edb0f0d294bb9b350bfb59a5fc4a2f934d55de5e195461e7b255784c3c70e9737f5caacbf6554871f4f037dc9567d34961f3b7ad73d1e7d2b20e790df65bc3c21ac1a91e3a82aed96c08ba762db0a9f21bec885d843ff71b65ee679225d",
    "vcode": "",
    "to": "http://www.shikee.com/"
}
response = requests.post(url, headers=headers, cookies=cookies, params=params, data=data, verify=False)

print(response.text)
print(response)