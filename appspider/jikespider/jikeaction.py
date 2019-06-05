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
            'platformName': PLATFORM_NAME,
            'deviceName': DEVICE_NAME,
            'appPackage': APP_PACKAGE,
            'appActivity': APP_ACTIVITY
        }
        self.driver = webdriver.Remote(DRIVER_SERVER,self.needed_params)
        self.waite = WebDriverWait(self.driver,TIMEOUT)

    def login_page(self):
        # 首先登陆qq 模拟登陆
        qqlogin = self.waite.until(EC.presence_of_element_located((By.ID,'com.ruguoapp.jike:id/tvPlatform')))
        qqlogin.click()
        login = self.waite.until(EC.presence_of_element_located((By.ID,'com.tencent.mobileqq:id/name')))
        login.click()
        # 获取动态页面
        start_page = self.waite.until(EC.presence_of_element_located((By.XPATH,'//android.widget.HorizontalScrollView[@id="com.ruguoapp.jike:id/tab_layout"]//android.widget.LinearLayout//androidx.appcompat.app.ActionBar.d[2]')))
        start_page.click()

    def get_now_user(self):
        # 检查当前全局元素是否已定位到
        # items = self.waite.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@recource-id="com.ruguoapp.jike:id/lay_ugc_header"]//android.widget.ImageView')))
        # 还是之前的位置
        self.driver.swipe(FLICK_START_X, FLICK_START_Y + FLICK_DISTANCE, FLICK_START_X, FLICK_START_Y)
        # 不需要全部 只需要一个
        item = self.waite.until(EC.presence_of_element_located((By.id,'//android.widget.RelativeLayout[@recource-id="com.ruguoapp.jike:id/lay_ugc_header"]//android.widget.ImageView')))
        return item

    def get_followers(self,elem):
        # 通过检查活动后效果没有改变从而退出循环
        old_items = []
        while True:
            # 需要检查是否已经全部显示
            new_items = self.waite.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@recource-id="com.ruguoapp.jike:id/gradual_mask"]//android.widget.ImageView')))
            if new_items != old_items:
                old_items = new_items
            else:
                # 当已经到达底端
                break
            # 设置一定等待时间
            sleep(SCROLL_SLEEP_TIME)
            # 可以控制屏幕滚动
            self.driver.swipe(FLICK_START_X, FLICK_START_Y + FLICK_DISTANCE, FLICK_START_X, FLICK_START_Y)


    def get_fans(self,elem):
        # 通过检查活动后效果没有改变从而退出循环
        old_items = []
        while True:
            # 需要检查是否已经全部显示
            new_items = self.waite.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@recource-id="com.ruguoapp.jike:id/gradual_mask"]//android.widget.ImageView')))
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
        for i in range(maxnum):
            self.login_page(i)
            useritem = self.get_now_user()
            useritem.click()
            fanslist = self.waite.until(EC.presence_of_element_located((By.ID,'com.ruguoapp.jike:id/scl_followed_count')))
            self.get_fans(fanslist)
            self.goback()
            followerslist = self.waite.until(EC.presence_of_element_located((By.ID,'com.ruguoapp.jike:id/scl_following_count')))
            self.get_followers(followerslist)
            self.goback()
            self.goback()

if __name__=='__main__':
    action = JikeAction()
    action.getusersinfo(MAXNUM)
