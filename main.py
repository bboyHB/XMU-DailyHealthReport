from selenium import webdriver
from time import sleep
from datetime import datetime

# 学号
student_id = '12345'
# 密码
password = 'xxxxx'
# 时间戳
time_stamp = "{0:%Y-%m-%d-%H-%M-%S/}".format(datetime.now())
# 日志
logfile = 'log.txt'


def report(uid, psw):
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
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
        print("OK")
    except:
        with open(logfile, 'a') as file_object:
            file_object.write("\n" + time_stamp + "----失败！！！！！！！")
        print("不OK")
    driver.quit()


def main():
    # 定时每天
    while True:
        # 判断是否达到设定时间，例如12:00
        while True:
            now = datetime.now()
            # 到达设定时间，结束内循环
            if now.hour == 12 and now.minute == 0:
                break
            # 不到时间就等20秒之后再次检测
            sleep(50)
        # 一天打卡一次
        report(student_id, password)


if __name__ == '__main__':
    main()
