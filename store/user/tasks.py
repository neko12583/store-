from store.celery import app
from tools.sms import YunTongXun
from django.conf import settings


# 任务函数
@app.task
def send_sms(phone, code):
    x = YunTongXun(settings.SMS_ACCOUNT_ID, settings.SMS_ACCOUNT_TOKEN,
                   settings.SMS_APP_ID, settings.SMS_TEMPLATE_ID)
    res = x.run(phone, code)
    return res
