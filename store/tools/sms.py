import datetime
import hashlib
import base64
import json
import requests  # 使用该库可以发出http请求


class YunTongXun():
    base_url = 'https://app.cloopen.com:8883'

    def __init__(self, accountSid, accountToken, appId, templateId):
        self.accountSid = accountSid
        self.accountToken = accountToken
        self.appId = appId
        self.templateId = templateId

    # 1 构造url
    def get_request_url(self, sig):
        # 这个url在云通讯的‘短信业务接口’页面的‘业务URL’里面复制的，然后再对应修改
        self.url = self.base_url + '/2013-12-26/Accounts/%s/SMS/TemplateSMS?sig=%s' % (self.accountSid, sig)
        return self.url

    # 2 生成时间戳
    def get_timestamp(self):
        now = datetime.datetime.now()
        now_str = now.strftime('%Y%m%d%H%M%S')
        return now_str

    # 3 生成加密并转成大写字母的sig，后面用来拼接给url
    def get_sig(self, timestamp):
        s = self.accountSid + self.accountToken + timestamp    # timestamp为时间戳
        md5 = hashlib.md5()
        md5.update(s.encode())  # 给s加密
        return md5.hexdigest().upper()   # 获取最终结果 并转换成大写  并返回

    # 4 构造请求头
    def get_request_header(self, timestamp):
        s = self.accountSid + ':' + timestamp
        b_s = base64.b64encode(s.encode()).decode()
        print(b_s)  # OGFhZjA3MDg3MzIyMjBhNjAxNzQzOTYxYjhjNTc2M2Y6MjAyMDA5MDYyMjA5MzE=
        return {
            'Accept': 'application/json',     # 写死
            'Content-Type': 'application/json;charset=utf-8',  # 写死
            'Authorization': b_s
        }

    # 5 请求体
    def get_request_body(self, phone, code):  # code是验证码
        data = {
            'to': phone,
            'appId': self.appId,
            'templateId': self.templateId,
            'datas': [code, '1']    # 这里的数字1，是发送给客户手机的短信提示内容‘请1分钟内输入验证码’
        }
        return data

    # 6 发送请求
    def do_request(self, url, header, body):
        res = requests.post(url, headers=header, data=json.dumps(body))
        return res.text

    # 7 完成短信发送
    def run(self, phone, code):
        timestamp = self.get_timestamp()   # 生成时间戳
        sig = self.get_sig(timestamp)   # 生成sig(sid+token+时间戳组成,并加密，转成大写)
        # 1 . url
        url = self.get_request_url(sig)   # 拼接出来url
        # 2. header
        header = self.get_request_header(timestamp)
        # 3 .body
        body = self.get_request_body(phone, code)
        # 4 .send request
        res = self.do_request(url, header, body)    # 这步是最重要的，其他的步骤都是为了给他生成参数
        return res   # res为容联云那边反馈回来的结果通常6个0代表发送成功


if __name__ == '__main__':
    aid = '8aaf0708732220a601743961b8c5763f'
    atoken = '957d47b86775416d9520760fead980f0'  # 这玩意每次都不一样
    appid = '8aaf0708732220a601743961b9807645'

    tid = '1'  # 短信模板，测试时值为 1    正式使用可在容联云上面创建模板
    x = YunTongXun(aid, atoken, appid, tid)
    res = x.run('13713788072', '654321')
    print(res)
