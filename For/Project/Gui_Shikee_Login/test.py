import requests


header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}

cookies = {'PHPSESSID': 'nsujoehapstiivkfa9vc4l7vn1', 'shikee': '%E7%81%AB%E9%92%B3%E5%88%98%E6%98%8E%7C1%7CuEdLL3cf494fbcNDCf%2BafiZfmxf4Xl5GJr31a%2FCQ8w8yNjLyUKGR0pbcq7jpdw%3D%3D', 'ci_session': 'a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22760f94be1c7511e873bd14699f0ed1d0%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A15%3A%22123.234.214.175%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A114%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F96.0.4664.45+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1675321129%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7Dda882215995ac27a49f48158f090e1d4'}

url = "http://user.shikee.com/buyer/join/pass_list"

response = requests.get(url = url, headers=header, cookies=cookies, verify=False)

print(response.text)
#print(response.json())