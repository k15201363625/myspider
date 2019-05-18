from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

server = 'http://localhost:4723/wd/hub'

desired_caps = {
    'platformName': 'Android',
    'deviceName': 'BLN_AL40',
    'appPackage': 'com.tencent.mm',
    'appActivity': '.ui.LauncherUI'
}

driver = webdriver.Remote(server, desired_caps)

wait = WebDriverWait(driver, 30)
login = wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/cjk')))
login.click()
phone = wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/h2')))
phone.set_text('15201363625')