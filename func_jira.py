import sys
import subprocess

try:
    from jira import JIRA
    import webbrowser

except:
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '-r', 'requirements.txt'])


import config
import path
import func_docx

from datetime import datetime
import time
import shutil
import os

# 기능 추가 할거 : 
# 1. txt 파일 내용 자동 작성 ㅇ
# 2. txt 파일로 해당이슈 댓글 달기 ㅇ
# 3. 구글 드라이브 경로에 파일 올리기 ㅇ
# 4. doc 문서 읽어서 내용 추가하기 ㅇ
# 5. 함수 별 시간 측정할 수있는 데코레이터 ㅇ
# 6. 매일 새벽에 할당된 이슈들 가져와서 이전이랑 기록 비교하려면? ㅁ

def logging_deco(func):
    def wrapped_func(*args):
        start_r = time.perf_counter()
        start_p = time.process_time()
        ret = func(*args)
        end_r = time.perf_counter()
        end_p = time.process_time()
        
        elapsed_r = end_r - start_r
        elapsed_p = end_p - start_p
        print(f'{func.__name__} : {elapsed_r:.6f}sec (Perf_Counter) / {elapsed_p:.6f}sec (Process Time)')
        return ret
    return wrapped_func


class Jira:
    def __init__(self):
        # Target Files
        self.file_path = path.file_path

        # Jira Connection
        self.url_prefix = config.jira_server + "/browse/"
        self.options = {'server': config.jira_server}
        self.jira = JIRA(self.options, basic_auth=config.jira_basic_auth)
        self.myid = config.jira_myid

        # Get All Project Key
        self.list_projects_key = []
        for project in self.get_projects():
            self.list_projects_key.append(project.raw['key'])
        
        self.site_contents = ""


    def make_template(self, site_code):
        site_name = path.dict_sitename[site_code]

        site_version = ""
        for x in os.listdir(self.file_path + f"/{site_code}"):
            if ".rpm" in x:
                site_version += x.split(".r")[0]+"\n"
            elif ".txt" in x:
                change_name = x
        
        site_contents = ""
        with open(self.file_path+"/" + site_code + "/" + change_name, "r", encoding="utf8") as file:
            for tmp in file.readlines():
                site_contents += tmp.replace("#", "")
        self.site_contents = site_contents

        jira_issue_link = []
        for x in [tmp.split("]")[0] for tmp in site_contents.replace(" ", "").split("[")]:
            if "-" not in x:
                continue
            jira_issue_link.append(x)

        download_link = path.dict_gdrive[site_code]
        
        jira_template = f"{site_name} ({site_code}) RPM 배포\n"
        jira_template += f"\n버전 : \n{site_version} \n" # get RPM으로 얻어와서 여러줄 추가
        jira_template += f"\n수정 내용 : \n{site_contents}\n" # get txt로 얻어와서 여러줄 추가
        jira_template += f"\n다운로드 경로 : \n{download_link}\n" # 업로드 경로가 다운로드 경로

        return jira_template, jira_issue_link

    def _search_issue(self, project, repoter):
        search_issue_jql = f"summary~AsyncError and project={project} and search_issue={repoter} and status not in (closed, done)"
        jira_issue = self.jira.search_issues(search_issue_jql)
        return jira_issue

    # 프로젝트 전체 목록 얻어오기 2022-09-08 테스트 성공
    def get_projects(self):
        return self.jira.projects()

    # 나에게 할당된 이슈들 링크, 제목, 지난 날짜를 알려줌 2022-09-08 테스트 성공
    @logging_deco
    def get_my_issue(self):
        #print(datetime.now(), " - 시작")
        list_res = []
        
        for x in self.list_projects_key:
            q = f'project = "{x}" AND assignee = {self.myid} ORDER BY created DESC'

            for iss in self.jira.search_issues(q):
                day = datetime.now() - datetime.strptime(iss.fields.created, '%Y-%m-%dT%H:%M:%S.%f%z').replace(tzinfo=None)
                list_tmp = [day.days, iss.key, iss.fields.summary]
                text = f"{day.days};[{iss.key}];{iss.fields.summary}"

                if "DEVOPS-" in text or "IOC-" in text:
                    continue

                list_res.append(list_tmp)

        #print(datetime.now(), " - 종료")
        return list_res

    
    # 특정 이슈에 댓글 달기 2022-09-08 테스트 성공
    def add_comment(self, issue_code, comment):
        comment_to_edit = self.jira.add_comment(issue_code, 'Change this content later')
        comment_to_edit.update(body=comment)

    # 특정 이슈 댓글 가져오기
    def get_comments(self, issue_code):
        return jira.comments(issue_code)

    # 특정 이슈의 담당자 변경
    def set_asignee(self):
        pass

    # 특정 이슈의 보고자 얻어오기
    def get_repoter(self):
        pass

    # 이슈 상태 변경
    def set_issue_statue(self):
        pass

    def get_issue_status(self):
        pass
    
    # docx에 수정 내용 추가하기
    def append_docx(self, file_name, contents):
        my_docx = func_docx.Docx()
        my_docx.append_contents(file_name, contents)


    # G-Drive 자동 업로드
    def upload_gdrive(self, site_code):
        # 사이트 코드로 업로드할 드라이브 경로 찾기
        for x in os.listdir(path.gdirve_path):
            if site_code in x:
                target_path = path.gdirve_path + "/" + x + "/패치"

        # 사이트 코드 경로 내부의 rpm 파일 다 가져오기
        source_path = []
        for x in os.listdir(path.file_path + "/" + site_code):
            if ".rpm" in x:
                source_path.append(path.file_path + "/" + site_code + "/" + x)

        # 구글 드라이브 데스크탑으로 업로드하기
        try:
            for x in source_path:
                shutil.copy(x, target_path)
                print(x, target_path)
            
            # 워드 내용 추가
            #self.append_docx(target_path+"/패치 내용.docx", datetime.datetime.now().strftime('%Y-%M-%d') + "\n" + self.site_contents)
            print(site_code + " 업로드 완료")

            #print(path.dict_gdrive[site_code])
            webbrowser.open(path.dict_gdrive[site_code])
        except:
            print(site_code + " 업로드 실패")


    # 템플릿 만들어서 JIRA 댓글 달기
    def auto_comment(self, site_code, white_list):
        if path.dict_gdrive[site_code] == "":
            print("다운로드 링크 없음")
        if path.dict_sitename[site_code] == "":
            print("사이트명 없음")

        # 사이트 코드가 있으면 템플릿을 만들어서 기록
        if site_code != "":
            str_template, issue_code_list = self.make_template(site_code)
            print(str_template)

        # 각 이슈 별로 댓글달고 웹페이지 열기, white_list 이슈코드에 있는 것만 달음, 중복 제거
        #prohibition_list = []
        for issue_code in list(set(issue_code_list)):
            if issue_code != "" and issue_code in white_list:
                self.add_comment(issue_code, str_template)

                print(config.jira_server + "/browse/" + issue_code)
                webbrowser.open(config.jira_server + "/browse/" + issue_code)


if __name__ == '__main__':
    jira = Jira()
    
    site_codes = ["KR"]
    white_list = ["YMSYS-293"]

    """
    # 2022-09-16 성공
    for site_code in site_codes:
        try:
            jira.upload_gdrive(site_code)
        except:
            print(site_code + " - upload err")

        #try:
        jira.auto_comment(site_code, white_list) 
        #except e:
            #print(site_code + " - comment err")
    """

    #나에게 할당된 이슈 가져오기
    for str_tmp in jira.get_my_issue():
        print(str_tmp)


'''
    # 이슈의 속성을 얻어오는 코드
    q = 'project = "이슈코드" ORDER BY created DESC'
    issues = jira.jira.search_issues(q)
    for iss in issues:
        o = jira.jira.issue(iss.key)
        for i in dir(iss.fields):
            if i == 'assignee' and "담당자" in str(getattr(iss.fields,i)):
                print(iss.key, " - " + iss.raw['fields'][i])))
        #print(o.assignee)

    iss = jira.jira.issue('이슈코드')
    for i in dir(iss.fields):
        print(i+":"+str(getattr(iss.fields,i)))
'''