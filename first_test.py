import requests
import pdb
from lxml import html
import urllib.request
from new_decoder import cjy_fetch_code
import time

db_url= "https://www.douban.com/group/topic/235035809/" #豆瓣帖子地址
db_url_commet = f"{db_url}add_comment"

headers = {
  'Cookie': '你的cookie',
  'User-Agent': '你的User-Agent',
  'Referer': 'https://www.douban.com/group/topic/235035809/?cid=4126293151',
  'Host': 'www.douban.com'
}

def my_job(rv_comment):
    params = {'ck': '你的ck',
              'rv_comment': rv_comment
              }
    # 获取网页信息，看看有没有验证码
    response = requests.post(db_url, headers=headers, data=params, verify=False).content.decode()
    selector = html.fromstring(response)
    captcha_image = selector.xpath("//img[@id=\"captcha_image\"]/@src")
    if(captcha_image):
        # 如果有验证码。。
        try:
            captcha_id = selector.xpath("//input[@name=\"captcha-id\"]/@value")
            print(captcha_id)
            test_case = f"https://www.douban.com/misc/captcha?id={captcha_id[0]}"
            filename = "target_image.jpeg"
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', '你的User-Agent')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(test_case, filename)
            im = open(filename, 'rb').read()
            correct_code = cjy_fetch_code(im, 3008)
            print(f"验证码：{correct_code}")
            params['captcha-id'] = captcha_id
            params['captcha-solution'] = correct_code
            res = requests.post(db_url_commet, headers=headers, data=params, verify=False)

            if '请正确输入图片中的单词' in res.text:
                print("验证码平台错误，等会儿重试吧......")
                time.sleep(10)
                my_job(rv_comment)
            else:
                print("应该是成功发送了捏")
                print(res.status_code)
        except:
            print("出了点问题，等会儿重试吧......")
            time.sleep(10)
            my_job(rv_comment)
    else:
        # 发起请求请求
        res = requests.post(db_url_commet, headers=headers, data=params, verify=False)
        print("毫无压力的发送了捏")
        print(res.status_code)

for i in range(5):
    my_job(f"喜欢我控赞{i}吗😎")
    time.sleep(10)
