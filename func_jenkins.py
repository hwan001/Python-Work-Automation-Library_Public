import sys
import subprocess

try:
    import requests
    import os

except:
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '-r', 'requirements.txt'])

import config


class Jenkins():
    def __init__(self):
        self.tmp = 1

    # 입력받은 정보로 item 생성
    def create_item(self, project_view, project_name):
        pass

    # 입력받은 프로젝트 명을 가진 item의 빌드를 api로 진행
    def build(self, project_view, project_name):
        #print(f"curl -X POST {config.jenkins_server}/view/" + project_view + "/job/" + project_name + f"/build --user {config.jenkins_user}:{config.jenkins_pw}")
        os.system(f"curl -X POST {config.jenkins_server}/view/" + project_view + "/job/" + project_name + f"/build --user {config.jenkins_user}:{config.jenkins_pw}")

if __name__ == '__main__':
    jenkins = Jenkins()
    #jenkins.build("asdf", "fda")




# job 생성
"{config.jenkins_server}/createItem?name=[job name]"

# job 조회
"{config.jenkins_server}/view/{project_view}/job/{project_name}/api/json" # or xml

# job 빌드 결과 조회
"{config.jenkins_server}/view/{project_view}/job/{project_name}/[build number]/api/json" # or xml

# job 빌드 결과 조회 - 마지막 성공 빌드
"{config.jenkins_server}/view/{project_view}/job/{project_name}/lastStableBuild/api/json" # or xml

# get job info 
"{config.jenkins_server}/view/{project_view}/api/json"