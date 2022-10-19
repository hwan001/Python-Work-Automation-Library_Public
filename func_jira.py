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
#import win32com

# 기능 추가 할거 : 
# 1. txt 파일 내용 자동 작성 ㅇ
# 2. txt 파일로 해당이슈 댓글 달기 ㅇ
# 3. 구글 드라이브 경로에 파일 올리기 ㅇ
# 4. doc 문서 읽어서 내용 추가하기 ㅇ
# 5. 함수 별 시간 측정할 수있는 데코레이터 ㅇ
# 기능 추가 할거 : 
# 6. 매일 아침 7시에 나한테 할당된 이슈들 가져와서 -> 메일이나 SNS로 전송해주기 (1.아웃룩, 2.카카오톡, 3.구글(smtp), 4.slack or teams)
# 7. 지라 이슈 asignee 변경 및 가져오기 기능
# 8. 지라 이슈 상태 가져오기 및 변경


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
        self.today_yyyymmdd = datetime.now().strftime('%Y-%m-%d')
        #self.template_string = ""
        #self.template_issue = ""

    # RPM 배포 템플릿 생성하기
    def make_template(self, site_code):
        site_name = path.dict_sitename[site_code]

        # 해당 사이트 코드 내부의 rpm 파일과 txt 파일 가져오기
        site_version = ""
        for x in os.listdir(self.file_path + f"/{site_code}"):
            if ".rpm" in x:
                site_version += x.split(".r")[0]+"\n"
            elif ".txt" in x:
                change_name = x
        
        # txt 파일 내용 가져오기
        site_contents = ""
        with open(self.file_path+"/" + site_code + "/" + change_name, "r", encoding="utf8") as file:
            for tmp in file.readlines():
                site_contents += tmp.replace("#", "")
        self.site_contents = site_contents

        # 내용 파싱해서 수정된 이슈코드 얻기
        jira_issue_link = []
        for x in [tmp.split("]")[0] for tmp in site_contents.replace(" ", "").split("[")]:
            if "-" not in x:
                continue

            jira_issue_link.append(x)

        # 해당 코드의 업로드 링크 참조 (미리 작성해둔 딕셔너리)
        download_link = path.dict_gdrive[site_code]
        
        jira_template = "*" + site_name + "(" + site_code + ") RPM 배포*\n"
        jira_template += f"\n버전 : \n{site_version} \n" # get RPM으로 얻어와서 여러줄 추가
        jira_template += f"\n수정 내용 : \n{site_contents}\n" # get txt로 얻어와서 여러줄 추가
        jira_template += f"\n다운로드 경로 : \n{download_link}\n" # 업로드 경로가 다운로드 경로

        self.template_string = jira_template
        self.template_issue = jira_issue_link
        
        return jira_template, jira_issue_link

    # jql을 사용한 이슈 검색
    @logging_deco
    def _search_issue(self, project, repoter):
        search_issue_jql = f"summary~AsyncError and project={project} and search_issue={repoter} and status not in (closed, done)"
        jira_issue = self.jira.search_issues(search_issue_jql)
        return jira_issue

    # 프로젝트 전체 목록 얻어오기 2022-09-08 테스트 성공
    def get_projects(self):
        return self.jira.projects()

    # 나에게 할당된 이슈들 링크, 제목, 지난 날짜를 알려줌 -> 2022-09-08 성공
    @logging_deco
    def get_my_issue(self):
        list_res = []
        
        for x in self.list_projects_key:
            q = f'project = "{x}" AND assignee = {self.myid} ORDER BY created DESC'

            for iss in self.jira.search_issues(q):
                day = datetime.now() - datetime.strptime(iss.fields.created, '%Y-%m-%dT%H:%M:%S.%f%z').replace(tzinfo=None)
                list_tmp = [day.days, iss.key, iss.fields.summary, config.jira_server + "/browse/" + iss.key]
                text = f"{day.days};[{iss.key}];{iss.fields.summary}"

                if "DEVOPS-" in text or "IOC-" in text or "H0194" in text:
                    continue

                list_res.append(list_tmp)

        return list_res

    
    # 특정 이슈에 댓글 달기 2022-09-08 테스트 성공
    def add_comment(self, issue_code, comment):
        comment_to_edit = self.jira.add_comment(issue_code, 'Change this content later')
        comment_to_edit.update(body=comment)

    # 특정 이슈 댓글 가져오기
    def get_comments(self, issue_code):
        return jira.comments(issue_code)

    def get_assignee(self, task_key):
        issue = self.jira.issue(task_key)
        return issue.fields.assignee.name

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
    
    # docx에 수정 내용 이어붙이기
    def append_docx(self, file_name, contents):
        my_docx = func_docx.Docx(file_name)
        my_docx.append_contents(contents)
    
    # G-Drive 자동 업로드 - 구버전용 이랑 구분할지?
    @logging_deco
    def upload_gdrive(self, site_code):
        # 사이트 코드로 업로드할 드라이브 경로 찾기
        for x in os.listdir(path.gdirve_path):
            if site_code + "_" in x:
                target_path = path.gdirve_path + "/" + x + "/패치"

        # 사이트 코드 경로 내부의 rpm 파일 다 가져오기
        source_path = []
        for x in os.listdir(path.file_path + "/" + site_code):
            if ".rpm" in x:
                source_path.append(path.file_path + "/" + site_code + "/" + x)
            elif ".txt" in x:
                change_name = x

        # 구글 드라이브 데스크탑으로 업로드하기
        try:
            for x in source_path:
                shutil.copy(x, target_path)
                #print(x, target_path)
            
            # 워드 내용 추가
            print(site_code + " - 업로드 완료")

            # 업로드한 페이지 열기
            webbrowser.open(path.dict_gdrive[site_code])
        except:
            print(site_code + " - 업로드 실패")


        # txt 파일 내용 가져오기
        site_contents = ""
        with open(self.file_path+"/" + site_code + "/" + change_name, "r", encoding="utf8") as file:
            for tmp in file.readlines():
                site_contents += tmp.replace("#", "")
        self.site_contents = site_contents

        # docx에 수정 내용 추가
        print("파일 명 : " + target_path + "/패치 내용.docx")
        self.append_docx(target_path + "/패치 내용.docx", self.site_contents + "\n")
            
    # 템플릿 만들어서 JIRA 댓글 달기
    @logging_deco
    def auto_comment(self, site_code, white_list):
        if path.dict_gdrive[site_code] == "":
            print("다운로드 링크 없음")

        if path.dict_sitename[site_code] == "":
            print("사이트명 없음")

        # 사이트 코드가 있으면 템플릿을 만들어서 기록
        #if self.template_string != "":
        #    str_template = self.template_string
        #    issue_code_list = self.template_issue
        if site_code != "":
            str_template, issue_code_list = self.make_template(site_code)
        else:
            print("site_code 없음")
            return

        # 각 이슈 별로 댓글달고 웹페이지 열기, white_list 이슈코드에 있는 것만, 중복 제거
        for issue_code in list(set(issue_code_list)):
            if issue_code != "" and (issue_code in white_list or "ALL" in white_list):
                self.add_comment(issue_code, str_template)

                print(config.jira_server + "/browse/" + issue_code)
                webbrowser.open(config.jira_server + "/browse/" + issue_code)


if __name__ == '__main__':
    jira = Jira()

    mode = 1
    white_list = [""]

    if mode == 1: # 지라 자동 배포 -> 2022-09-16 성공
        site_codes = []
        for x in os.listdir(path.file_path):
            if os.path.isdir(path.file_path + "/" + x):
                site_codes.append(x)

        for site_code in site_codes:
            jira.upload_gdrive(site_code)
            jira.auto_comment(site_code, white_list) 

    elif mode == 2: #오래된 순서로 나에게 할당된 이슈 가져오기 -> 2022-09-26 성공
        cnt = 0
        str_res = ""
        file_path =  path.home_path + f"/Desktop/MyIssue_{jira.today_yyyymmdd}.txt" # 파일명, 경로 변경 필요 (날짜 넣기)
        print(file_path)

        for str_tmp in list(reversed(sorted(jira.get_my_issue(), key=lambda x:x[0]))):
            str_res += str(str_tmp) + "\n"
            cnt+=1

        str_res += "count :" + str(cnt)
        print(str_res)

        with open(file_path, "w") as f:
            f.write(str_res)

    elif mode == 3: # [예시] 이슈의 속성을 얻어오는 코드 -> 안돌아감, 샘플코드임
        q = 'project = "이슈코드" ORDER BY created DESC'
        issues = jira.jira.search_issues(q)
        for iss in issues:
            o = jira.jira.issue(iss.key)
            for i in dir(iss.fields):
                if i == 'assignee' and "담당자" in str(getattr(iss.fields,i)):
                    print(iss.key, " - " + iss.raw['fields'][i])
            print(o.assignee)

        iss = jira.jira.issue('이슈코드')
        for i in dir(iss.fields):
            print(i+":"+str(getattr(iss.fields,i)))
    
    elif mode == 4: # [작성중]구버전 배포 -> 안돌아감
        # 경로 입력받기
        path_target = path.home_path + "/Desktop/old_version"
        versions = []
        for x in os.listdir(path_target):
            if os.path.isdir(path_target + "/" + x):
                versions.append(x)
        
        print([path.dict_gdrive_version[version] for version in versions])
        white_list = [""]
