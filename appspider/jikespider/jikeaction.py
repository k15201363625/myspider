from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from config import *

# 使用selenium进行高级控制

class JikeAction(object):
    def __init__(self):
        '''
        initialization config
        '''
        # 驱动
        self.needed_params={
            # "deviceName": DEVICE_NAME,
            # "platformName": PLATFORM_NAME,
            # "appActivity": APP_ACTIVITY,
            # "appPackage": APP_PACKAGE
            "deviceName": "Google_Nexus_5",
            "platformName": "Android",
            "appActivity": ".ui.activity.RgFragHubActivity",
            "appPackage": "com.ruguoapp.jike"
        }
        self.driver = webdriver.Remote(DRIVER_SERVER,self.needed_params)
        self.waite = WebDriverWait(self.driver,TIMEOUT)
        # 已经爬取过关注粉丝列表的用户
        self.visitedUsers = []

    def login_page(self):
        # 首先登陆qq 模拟登陆
        qqlogin = self.waite.until(EC.presence_of_element_located((By.XPATH,'//*[@resource-id="com.ruguoapp.jike:id/login_flexbox"]//android.widget.FrameLayout[2]')))
        qqlogin.click()
        # login_1 = self.waite.until(EC.presence_of_element_located((By.ID,'com.tencent.mobileqq:id/login')))
        # login_1.click()
        login_2 = self.waite.until(EC.presence_of_element_located((By.XPATH,'//android.widget.Button[@resource-id="com.tencent.mobileqq:id/name"]')))
        login_2.click()
        # 获取动态页面
        start_page = self.waite.until(EC.presence_of_element_located((By.XPATH,'//*[@resource-id="com.ruguoapp.jike:id/tab_layout"]//android.widget.LinearLayout//androidx.appcompat.app.ActionBar.d[2]')))
        start_page.click()

    def get_now_user(self):
        # 检查当前全局元素是否已定位到
        # items = self.waite.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@recource-id="com.ruguoapp.jike:id/lay_ugc_header"]//android.widget.ImageView')))
        self.waite.until(EC.presence_of_element_located((By.ID,'com.ruguoapp.jike:id/gradual_mask')))
        # 还是之前的位置
        self.driver.swipe(FLICK_START_X, FLICK_START_Y + FLICK_DISTANCE, FLICK_START_X, FLICK_START_Y)
        # 不需要全部 只需要一个
        item = self.waite.until(EC.presence_of_element_located((By.XPATH,'//android.widget.RelativeLayout[@resource-id="com.ruguoapp.jike:id/lay_ugc_header"]//android.widget.ImageView')))
        # 避免获取同一个用户的关注粉丝列表 所以需要进行用户判断

        return item

    def get_followers(self):
        # 通过检查活动后效果没有改变从而退出循环
        old_items = []
        while True:
            # 需要检查是否已经全部显示
            new_items = self.waite.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@resource-id="com.ruguoapp.jike:id/gradual_mask"]//android.widget.ImageView')))
            if new_items != old_items:
                old_items = new_items
            else:
                # 当已经到达底端
                break
            # 设置一定等待时间
            sleep(SCROLL_SLEEP_TIME)
            # 可以控制屏幕滚动
            self.driver.swipe(FLICK_START_X, FLICK_START_Y + FLICK_DISTANCE, FLICK_START_X, FLICK_START_Y)


    def get_fans(self):
        # 通过检查活动后效果没有改变从而退出循环
        old_items = []
        while True:
            # 需要检查是否已经全部显示
            # new_items = self.waite.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@recource-id="com.ruguoapp.jike:id/gradual_mask"]//android.widget.ImageView')))
            
            new_items = self.waite.until(EC.presence_of_all_elements_located((By.ID,'com.ruguoapp.jike:id/iv_avatar')))

            if new_items != old_items:
                old_items = new_items
            else:
                # 当已经到达底端
                break
            # 设置一定等待时间
            sleep(SCROLL_SLEEP_TIME)
            # 可以控制屏幕滚动
            self.driver.swipe(FLICK_START_X, FLICK_START_Y + FLICK_DISTANCE, FLICK_START_X, FLICK_START_Y)
    
    def scroll(self):
        # 模拟拖动
        while True:
            self.driver.swipe(FLICK_START_X, FLICK_START_Y + FLICK_DISTANCE, FLICK_START_X, FLICK_START_Y)
            sleep(SCROLL_SLEEP_TIME) #设置等待分析的时间

    def goback(self):
        driver.back()
        sleep(GOBACK_SLEEP_TIME)
    
    def getusersinfo(self,maxnum):
        self.login_page()
        for i in range(maxnum):
            useritem = self.get_now_user()
            useritem.click()
            username = self.waite.until(EC.presence_of_element_located((By.ID,'com.ruguoapp.jike:id/tv_username'))).get_attribute('text')
            print('now username is:'+ username + '\n')
            if username in self.visitedUsers:
                self.goback()
                continue
            else:
                self.visitedUsers.append(username)
                fanslist = self.waite.until(EC.presence_of_element_located((By.ID,'com.ruguoapp.jike:id/scl_followed_count')))
                fanslist.click()
                self.get_fans()
                self.goback()
                followerslist = self.waite.until(EC.presence_of_element_located((By.ID,'com.ruguoapp.jike:id/scl_following_count')))
                followerslist.click()
                self.get_followers()
                self.goback()
                self.goback()

if __name__=='__main__':
    action = JikeAction()
    action.getusersinfo(MAXNUM)
