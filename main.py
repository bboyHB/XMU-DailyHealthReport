from selenium import webdriver
from time import sleep
from datetime import datetime

"""
程序每天凌晨会将签到状态重置
从早上7点到下午6点每隔一小时会检测一下是否签到
若是当天已经签到，就会跳过；
若没有签到，就会执行签到，若是签到失败，程序就会过一个小时再试。
"""

# 学号
student_id = '12345'
# 密码
password = 'xxxxx'
# 日志
logfile = 'log.txt'


def report(uid, psw):
    time_stamp = "{0:%Y-%m-%d-%H-%M-%S/}".format(datetime.now())
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    success = True
    try:
        driver.get("http://xmuxg.xmu.edu.cn/xmu/app/214")
        sleep(5)
        driver.find_element_by_xpath("//button[contains(text(), '统一身份认证')]").click()
        sleep(5)
        driver.find_element_by_id('username').send_keys(uid)
        driver.find_element_by_id('password').send_keys(psw)
        driver.find_element_by_xpath("//button[contains(text(), '登录')]").click()
        sleep(5)
        driver.find_element_by_xpath("//div[contains(text(), 'Daily Health Report 健康打卡')]").click()
        sleep(10)
        windows = driver.window_handles
        driver.switch_to.window(windows[-1])
        driver.find_element_by_xpath("//div[contains(text(), '我的表单')]").click()
        sleep(5)
        driver.find_element_by_xpath("//*[@id='select_1582538939790']/div/div").click()
        sleep(5)
        driver.find_element_by_xpath("//label[@title='是 Yes']").click()
        sleep(5)
        driver.find_element_by_class_name('form-save').click()
        sleep(5)
        alert = driver.switch_to.alert
        alert.accept()

        with open(logfile, 'a') as file_object:
            file_object.write("\n" + time_stamp + "----成功")
        print(time_stamp + "-OK")
    except:
        with open(logfile, 'a') as file_object:
            file_object.write("\n" + time_stamp + "----失败！！！！！！！")
        print(time_stamp + "-不OK")
        success = False
    driver.quit()
    return success


def main(done_today=False):
    # 定时每天
    while True:
        # 判断是否达到设定时间
        while True:
            now = datetime.now()
            # 每小时检查一次
            if not done_today and 7 <= now.hour <= 18 and now.minute == 0:
                break
            # 每天凌晨1点重置
            if now.hour == 1 and 0 <= now.minute <= 1:
                done_today = False
            # 不到时间就等60秒之后再次检测
            sleep(60)
        # 一天打卡一次
        if not done_today:
            done_today = report(student_id, password)


if __name__ == '__main__':
    # 若今天已经打卡，就main(True)，否则就main()，防止每小时都自动跳浏览器出来
    main(True)
