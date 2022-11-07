import selectors
import sys
import subprocess

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.alert import Alert
    from selenium.webdriver.common.by import By
    

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

        #self.company_branch_url = f"{config.gerrit_host}/gitweb?p=onenet/company_code.git;a=blob;f=ftc_companyName.csv;h=802c5cc6b2867547b4486d21fd8ec1d2e98e327b;hb=refs/heads/master"

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

    def 교육영상넘기기(self):
        import pyautogui
        baseurl = "https://www.kehrd.com/study/study.html?no=559952&num=1&max_num=0&user_id1=hunesion8306"
        self.chrome_driver.get(baseurl)

        pop_study = self.chrome_driver.find_element(By.CLASS_NAME, 'pop_study')
        pop_study = pop_study.find_element(By.CLASS_NAME, 'study_left')
        pop_study = pop_study.find_element(By.CLASS_NAME, 'study_video')
        
        self.chrome_driver.switch_to.frame("frame")
        
        while 1:
            style_play = self.chrome_driver.find_element(By.XPATH, '//*[@id="play"]')
            print(style_play.value_of_css_property("style"))
            time.sleep(3)
        #print("btn_pause.png", "btn_pause.png" in style_play.get_attribute("style"))
        #print("btn_play.png", "btn_play.png" in style_play.get_attribute("style"))

        while False:
            style_play = self.chrome_driver.find_element(By.XPATH, '//*[@id="play"]')
            if "btn_pause.png" in style_play.get_attribute("style"):
                pyautogui.click(1256, 791) # Next
                #self.chrome_driver.find_element(By.XPATH, '//*[@id="next"]')
                #self.chrome_driver.execute_script("arguments[0].click();", self.chrome_driver.find_element(By.XPATH, '//*[@id="next"]'))
                
                print("NEXT 클릭")
            else:
                print("대기 - 재생 중")
                time.sleep(10)

if __name__ == '__main__':
    selenium = Selenium()
    selenium.교육영상넘기기()
