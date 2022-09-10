import sys
import subprocess

try:
    from distutils.command.build import build
    import json
    from urllib.request import HTTPBasicAuthHandler, HTTPPasswordMgrWithDefaultRealm, build_opener, install_opener, urlopen
    import requests

    import time
    import datetime
    import winsound as ws
    import ctypes

except:
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '-r', 'requirements.txt'])


import config


class Gerrit():
    def __init__(self):
        # Target Files
        self.path_rpm = config.path_rpm
        

    # gerrit REST API
    def send_api(self, path, method):
        host = config.gerrit_host + "/a"
        url = host + path

        headers = {'Content-Type':'application/json', 'charset':'UTF-8'}
        body = {
            "key1":"value1",
            "key2":"value2"
        }
        auth = requests.auth.HTTPDigestAuth(config.gerrit_username, config.gerrit_token)

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, auth=auth)
            elif method == 'POST':
                response = requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t"), auth=auth)
            elif method == 'PUT':
                response = requests.put(url, auth=auth)

            return json.loads(response.text[4:] if response.text.startswith(')]}\'') else response.text)

        except:
            pass


    # CodeReview Check
    def Check_CodeReview(self, sec=20):
        while(sec):
            try:
                str_status, str_text = self.send_api("/changes/?q=project:onenet/rpm+reviewer:self+is:open", "GET")
                str_text = str_text.replace(")]}'", "").strip()

                #print(str_text)
                if(len(str_text) < 10):
                    print(datetime.datetime.now(), ' - 없음')
                    time.sleep(sec)

                else:
                    print(datetime.datetime.now(), ' - 있음', str_text)
                    self.msgbox("Check your code review job", "Notice : Gerrit")

                    # 코드리뷰 페이지 열어주고 소리내기
                    for i in range(5):
                        ws.beep(2000, 1000)

            except:
                pass
            


    # windows MessageBox  
    def msgbox(self, str_msg, str_title):
        ctypes.windll.LoadLibrary("user32.dll").MessageBoxW(0, str_msg, str_title, 1)



    def tmp_check_branchName(self, str):
        url = ""

        #return True
        return False


    def download_CsvFile(self):
        url = ""
        user = ""
        pw = ""

        with urlopen(url, auth=(user, pw)) as f:
            html = f.read().decode('utf-8')

        print(html) 
        #with open(file_name, "wb") as file:


    # 특정 상태의 커밋을 스캔해옴
    def scan_CommitStatus1(self, status):
        str_text = ""
        str_status = ""

        str_status, str_text = self.send_api("/changes/?q=is:"+status, "GET")
        str_text = str_text.split(")]}'")[1].strip("'<>() ").replace("\'", "\"") # .split(")]}'")[1]
        list_text = str_text.split("},")

        for text in list_text:
            #jDump = json.dumps(text, indent=2, ensure_ascii=False)
            jLoad = json.loads(text+"},", strict=False)
            print("line : ", jLoad["id"])
            #print(text+" }\n")

        print(len(list_text))


    # project:onenet/rpm -age:7d:  # 기간과 프로젝트로 조회
    def scan_CommitStatus(self, status):
        try:
            str_status, str_text = self.send_api("/changes/?q=" + status + "/detail", "GET")
            str_text = str_text.replace(")]}'", "").strip()

            #print(str_status+"\n")
            #print(str_text)

        except:
            pass
            
            

    #프로젝트 목록 받아오기
    def get_projects(self):
        list_onenet_project_file = []
        json_tmp = self.send_api("/projects/?d", "GET")

        for tmp in json_tmp:
            try:
                str_tmp = tmp#.split("release-")[1]
                if ("onenet/" in str_tmp) and ("UC" not in str_tmp):
                    list_onenet_project_file.append(str_tmp)
            except:
                pass

        print(list_onenet_project_file)



if __name__ == '__main__':
    gerrit = Gerrit()
