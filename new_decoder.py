from hashlib import md5
import requests
# 超级鹰参数
cjy_params = {
    'user': '超级鹰用户名',
    'pass2': md5('超级鹰密码'.encode('utf8')).hexdigest(),
    'softid': '96001',
}
# 超级鹰请求头
cjy_headers = {
    'Connection': 'Keep-Alive',
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
}
# 超级鹰识别验证码
def cjy_fetch_code(im, codetype):
    cjy_params.update({'codetype': codetype})
    files = {'userfile': ('ccc.jpg', im)}
    resp = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=cjy_params, files=files,
                  headers=cjy_headers).json()
    print(f"here is the request: {resp}")
    # 错误处理
    if resp.get('err_no', 0) == 0:
        return resp.get('pic_str')

# 调用代码
if __name__ == '__main__':
    im = open('captcha.jpeg', 'rb').read()
    print(cjy_fetch_code(im, 1902))