from celery import Celery
from django.conf import settings
import os

# 1 设置环境变量,告诉celery为哪一个django项目服务
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
# 2 创建app(Celery对象)
app = Celery('store')
# 3 再配置
app.conf.update(
    BROKER_URL='redis://@127.0.0.1:6379/1'  # 任务队列
)
# 4 告知celery 去哪个应用的目录下找任务函数
app.autodiscover_tasks(settings.INSTALLED_APPS)
