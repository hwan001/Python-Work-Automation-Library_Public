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
    
    import os

except:
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '-r', 'requirements.txt'])


import config


class Gerrit():
    def __init__(self):
        pass

    # gerrit REST API
    def send_api(self, path, method, body={}):
        host = config.gerrit_host + "/a"
        url = host + path

        headers = {'Content-Type':'application/json', 'charset':'UTF-8'}
        auth = requests.auth.HTTPDigestAuth(config.gerrit_username, config.gerrit_token)

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, auth=auth)
            elif method == 'POST':
                if body is None:
                    return
                
                response = requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t"), auth=auth)
            elif method == 'PUT':
                response = requests.put(url, auth=auth)

            return json.loads(response.text[4:] if response.text.startswith(')]}\'') else response.text)

        except:
            pass

    # 사용법 및 테스트 필요
    def submit_change(self, id):
        api_query = "/changes/" + id + "/submit"
        body = {
            "wait_for_merge":True
        }
        
        try:
            json_res = self.send_api(api_query, "POST", body=body)
            
        except Exception as ex:
            print(ex)

        
    # CodeReview Check
    def Check_CodeReview(self, sec=20):
        while(sec):
            try:
                str_status, str_text = self.send_api("/changes/?q=project:projcet/rpm+reviewer:self+is:open", "GET")
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

    def get_all_siteBranch(self):
        list_hyphen_version = []
        json_tmp = self.send_api("/projects/projcet%2Frpm/branches", "GET")

        for tmp in json_tmp:
            try:
                str_tmp = tmp['ref'].split("release")[1]
                if "/" not in str_tmp or "-" not in str_tmp:
                    continue
                if "DEVOPS" in str_tmp:
                    continue
                list_hyphen_version.append("release"+str_tmp)
            except:
                pass
        
        return list_hyphen_version

    def get_all_siteCode(self):
        list_hyphen_version = []
        json_tmp = self.send_api("/projects/projcet%2Frpm/branches", "GET")

        for tmp in json_tmp:
            try:
                str_tmp = tmp['ref'].split("release")[1][1:]
                if "-" not in str_tmp:
                    continue
                if "DEVOPS" in str_tmp:
                    continue
                list_hyphen_version.append(str_tmp)
            except:
                pass
            
        dict_tmp = {}
        for x in list_hyphen_version:
            dict_tmp[x.split("-")[1]] = ""
        
        return list(dict_tmp.keys())

    #프로젝트 목록 받아오기
    def get_projects(self):
        list_project_file = []
        json_tmp = self.send_api("/projects/?d", "GET")

        for tmp in json_tmp:
            try:
                str_tmp = tmp#.split("release-")[1]
                if ("projcet/" in str_tmp) and ("UC" not in str_tmp):
                    list_project_file.append(str_tmp)
            except:
                pass

        print(list_project_file)
        return list_project_file
            
            
    # 특정 Change의 커밋 메시지를 가져옴
    def get_revisions_id(self):
        api_query = "/changes/?q=project:projcet/rpm+reviewer:self+is:open"
        list_res = []

        try:
            json_res = self.send_api(api_query, "GET")
            for json_tmp in json_res:
                list_res.append(json_tmp['id'])

        except Exception as ex:
            print(ex)

        return list_res

    def get_id(self, id):
        api_query = "/changes/" + id

        try:
            json_res = self.send_api(api_query, "GET")
            return json_res

        except Exception as ex:
            print(ex)
    
    # 특정 Change의 정보를 json으로 받아옴 (내가 올린것만)
    def get_subject(self, id):
        api_query = "/changes/" + id

        try:
            json_res = self.send_api(api_query, "GET")
            if json_res['owner']['_account_id'] == config.gerrit_user_id:
                return json_res

        except Exception as ex:
            print(ex)



# 코드리뷰 대기 중인 change들 내용을 특정 경로에 파일로 생성해줌 
# -> 빌드 후 이것도 같이 넘기면 작성 편함
def make_detail_file():
    gerrit = Gerrit()
    date = str(datetime.datetime.now()).split(" ")[0] 
    file_path = config.path_rpm + "/" + date
    
    try:
        os.mkdir(file_path)
        
    except:
        pass
    
    for id in gerrit.get_revisions_id():
        json_tmp = gerrit.get_subject(id)
        
        if json_tmp == None:
            continue
        
        str_subject = json_tmp["subject"]
        str_branch = str(json_tmp["branch"]).replace("release/", "")
        
        # 일부 버전 확인 후 예외처리 로직 필요
        if "-" not in str_branch:
            continue
            
        try:
            file_name = file_path + "/" + str_branch + ".txt"
            file_content = str(str_subject).replace("[", "\n[")[1:]
            
            print("file : ", file_name)
            
            #with open(file_name, "w") as file:
            #    file.write(file_content)

        except:
            print(str_branch, " - err")



if __name__ == '__main__':
    gerrit = Gerrit()
    
    list_tmp = []
    for x in list_tmp:
        json_tmp = gerrit.get_id(x)
        prefix_tmp = json_tmp['project'].replace("/", "_")
        tmp = json_tmp['branch'].split("/")[1].split("-")
        suffix_tmp = tmp[0] + ".0 -> " + tmp[0] + ".1"
        site_code = tmp[1]
        
        print(prefix_tmp + "-" + suffix_tmp)
        #q = "/changes/" + json_tmp['id'] + "/COMMIT_MSG"
        #print(gerrit.send_api(q, "GET"))
        
        # 작동은 되지만 사용은 x
        #gerrit.submit_change(x)
    
    #gerrit.get_revisions_id()