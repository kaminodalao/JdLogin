from selenium import webdriver
import time
import os
import sys
import requests
import json
import subprocess

REPORTURL = os.getenv("REPORTURL")
TASKID = os.getenv("TASKID")

start_time = int(time.time())


def report(data):
    print("report %s" % str(data))
    if REPORTURL is None:
        return
    try:
        response = requests.post(REPORTURL, json={
            'data': data,
            'taskid': TASKID,
            'runtime': int(time.time()) - start_time
        }, timeout=5)
        
        return json.loads(response.content.decode('utf8'))
        try:
            global driver
            data = json.loads(response.content.decode('utf8'))
            if 'sendkeys' in data and data['sendkeys'] is not None:
                driver.send_keys(data['sendkeys'])
        except Exception as ei:
            print("输入文本失败" % ei)
    except Exception as e:
        print("report error %s" % str(e))
        return {}


report({'name': 'TASK_STARTED', 'code': 1})

options = webdriver.EdgeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--kiosk")
options.add_argument("--proxy-server=http://10.8.0.3:7891")
driver = webdriver.Edge(options=options)
print(os.getenv("TEST"))
print("打开登陆页面")
report({'name': 'START_OPEN_LOGIN_PAGE', 'code': 1})
driver.get("https://home.m.jd.com/myJd/home.action")

in_login_page = False

for _ in range(20):
    if 'plogin.m.jd.com' in driver.current_url:
        print("成功进入登陆页面")
        report({'name': 'OPEN_LOGIN_PAGE_SUCCESS', 'code': 1})
        in_login_page = True
        break
    time.sleep(1)

if in_login_page is False:
    print("进入登陆页面失败")
    report({'name': 'OPEN_LOGIN_PAGE_FAIL', 'code': -1})
    sys.exit()

print("开始检测登录状态")
report({'name': 'START_CHECK_LOGIN_STATUS', 'code': 1})

is_login_success = False

for _ in range(600):
    if driver.current_url == 'https://home.m.jd.com/myJd/home.action':
        print("登陆成功")
        report({'name': 'LOGIN_SUCCESS', 'code': 1})
        cookie_list = driver.get_cookies()
        report({'name': 'COOKIE_VALUE', 'code': 1})
        is_login_success = True
        break
    print("正在检测登录")
    data = report({'name': 'CHECKING_LOGIN_STATUS', 'code': 1})
    try:
        if 'sendkeys' in data and data['sendkeys'] is not None:
            report({"getkey":data['sendkeys'],"code":1})
            driver.send_keys(data['sendkeys'])
    except Exception as _:
        pass
    time.sleep(1)

if is_login_success is False:
    print("超时退出")
    report({'name': 'LOGIN_TIMEOUT', 'code': -1})

else:
    print("任务完成退出")
    report({'name': 'LOGIN_FINISHED', 'code': 0,
           'cookie': json.dumps(cookie_list)})
