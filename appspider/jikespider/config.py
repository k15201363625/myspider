'''
爬虫配置文件
'''
# APPIUM config
DRIVER_SERVER = 'http://localhost:4723/wd/hub'

DEVICE_NAME = "Google_Nexus_5"
PLATFORM_NAME = "Android"
APP_ACTIVITY = ".ui.activity.RgFragHubActivity"
APP_PACKAGE = "com.ruguoapp.jike"

TIMEOUT = 300

# 滑动控制点
FLICK_START_X = 500
FLICK_START_Y = 200
FLICK_DISTANCE = 800
# TouchAction(driver)   .press(x=519, y=948)   .move_to(x=522, y=856)   .release()   .perform()
# TouchAction(driver)   .press(x=590, y=709)   .move_to(x=587, y=619)   .release()   .perform()

# 滑动间隔
SCROLL_SLEEP_TIME = 1.5
GOBACK_SLEEP_TIME = 0.5

# 总的起始人数目
MAXNUM = 10

#mongodb 数据库链接存储信息设置
MONGO_HOST = 'localhost'
MONGO_DATABASE = 'jike'
TABLE_NAME = 'userinfo'
