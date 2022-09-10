import sys
import subprocess

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.alert import Alert

    import time

except:
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '-r', 'requirements.txt'])


import config



class Selenium():
    def __init__(self):
        chrome_option = Options()
        chrome_option.add_argument('--headless')
        chrome_option.add_argument('--log-level=3')
        chrome_option.add_argument('--disable-logging')
        chrome_option.add_argument('--no-sandbox')
        chrome_option.add_argument('--disable-gpu')

        chrome_option.add_argument('--ignore-certificate-errors')
        chrome_option.add_argument('--ignore-ssl-errors')

        chrome_driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options = chrome_option)
        self.chrome_driver = chrome_driver

        self.company_branch_url = f"{config.gerrit_host}/gitweb?p=onenet/company_code.git;a=blob;f=ftc_companyName.csv;h=802c5cc6b2867547b4486d21fd8ec1d2e98e327b;hb=refs/heads/master"


    def selenium_1(self):
        self.chrome_driver.get(self.company_branch_url)

        self.chrome_driver.quit()


    def check_branchName(self, str_company):
        self.chrome_driver.get(self.company_branch_url)

        time.sleep(3000) 
        self.chrome_driver.switch_to.window()

        try:
            input_id = self.chrome_driver.find_element_by_xpath('//*[@id="j_username"]')
            input_id.send_keys('test')

        except Exception as err:
            print(err)

        btn_login = self.chrome_driver.find_element_by_css_selector('input.btn.btn-primary')
        btn_login.click()

        time.sleep(3000)

        return False


    def test_check_alert(self, id, pw):
        baseurl = config.gerrit_host + "/login/#/"

        wait = WebDriverWait(self.chrome_driver, 30)

        self.chrome_driver.get(baseurl)

        time.sleep(3)


        #webdriver.ActionChains(dr).send_keys(id+Keys.TAB).perform()

        #pyautogui.moveTo(1000, 700, 1)

        #alert = wait.until(EC.alert_is_present())

        #alert.send_keys(id)
        #alert.send_keys(Keys.TAB)
        #alert.send_keys(pw)

        #alert.accept()

        #print("hjjhk  ", dr.switch_to.active_element.text, "  hjkhjk")
        #dr.switch_to().alert().send_keys(f"{config.jenkins_user}")
        #dr.switch_to().alert().send_keys(f"{config.jenkins_pw}")

        time.sleep(1)

        return True


if __name__ == '__main__':
    selenium = Selenium()
