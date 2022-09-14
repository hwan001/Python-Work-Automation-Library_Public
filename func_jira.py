import sys
import subprocess

try:
    from jira import JIRA
    from datetime import datetime

except:
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '-r', 'requirements.txt'])


import config
import path
import os

# 기능 추가 할거 : 
# 1. txt 파일 내용 자동 작성
# 2. txt 파일로 해당이슈 댓글 달기
# 3. 구글 드라이브 경로에 파일 올리기
# 4. doc 문서 읽어서 내용 추가하기
# 5. 함수 별 시간 측정할 수있는 데코레이터
# 6. 매일 새벽에 할당된 이슈들 가져와서 이전이랑 기록 비교하려면?

class Jira:
    def __init__(self):
        # Target Files
        self.file_path = path.file_path

        # Jira Connection
        self.url_prefix = config.jira_server+"/browse/"
        self.options = {'server': config.jira_server}
        self.jira = JIRA(self.options, basic_auth=config.jira_basic_auth)
        self.myid = config.jira_myid

        # Get All Project Key
        self.list_projects_key = []
        for project in self.get_projects():
            self.list_projects_key.append(project.raw['key'])
        

    def make_template(self, site_code):
        site_name = path.dict_sitename[site_code]

        site_version = "" # rpm 파일 불러오기
        for x in os.listdir(self.file_path + f"/{site_code}"):
            if ".rpm" in x:
                site_version += x.split(".r")[0]+"\n"
            elif ".txt" in x:
                change_name = x
        
        site_contents = ""
        with open(f"{self.file_path}/{site_code}/{change_name}", "r") as file:
            for tmp in file.readlines():
                site_contents += tmp.replace("#", "")

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
    def get_my_issue(self):
        print(datetime.now(), " - 시작")
        list_res = []

        for x in self.list_projects_key:
            q = f'project = "{x}" AND assignee = {self.myid} ORDER BY created DESC'

            for iss in self.jira.search_issues(q):
                day = datetime.now() - datetime.strptime(iss.fields.created, '%Y-%m-%dT%H:%M:%S.%f%z').replace(tzinfo=None)
                #list_tmp = [day.days, ]
                text = f"{day.days};[{iss.key}];{iss.fields.summary}"

                if "DEVOPS-" in text or "IOC-" in text:
                    continue

                list_res.append(text)

        print(datetime.now(), " - 종료")
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

    # 특정 폴더에 있는 RPM 파일 목록 얻어오기
    def get_rpmfilenames(self):
        pass
    
    def tmp_func(self):
        str_name = ""
        if str_name != "":
            str_template, issue_code_list = self.make_template(str_name)
            print(str_template)

        for issue_code in list(set(issue_code_list)):
            if issue_code != "":
                print("https://hunesion.atlassian.net/browse/" + issue_code)
                self.add_comment(issue_code, str_template)


if __name__ == '__main__':
    jira = Jira()

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