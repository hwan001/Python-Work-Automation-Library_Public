from genericpath import isdir
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

def TEST(func):
    def wrapped_func(*args):
        print("*********************테스트 중인 함수입니다.*********************")
        ret = func(*args)
        print("*********************결과를 보장할 수 없음.*********************")
        return ret
    return wrapped_func

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


    @TEST
    def _search_issue(self, project, repoter): # jql을 사용한 이슈 검색
        search_issue_jql = f"summary~AsyncError and project={project} and search_issue={repoter} and status not in (closed, done)"
        jira_issue = self.jira.search_issues(search_issue_jql)
        return jira_issue

    @TEST
    def get_comments(self, issue_code): # 특정 이슈 댓글 가져오기
        return self.comments(issue_code)

    @TEST
    def get_assignee(self, task_key): # 해당 이슈의 담당자를 얻어옴
        issue = self.jira.issue(task_key)
        return issue.fields.assignee.name

    @TEST
    def set_asignee(self): # 특정 이슈의 담당자 변경
        pass

    @TEST 
    def get_repoter(self): # 특정 이슈의 보고자 얻어오기
        pass

    @TEST 
    def set_issue_statue(self): # 이슈 상태 변경
        pass

    @TEST
    def get_issue_status(self): # 이슈 상태 얻기
        pass
    

    def get_projects(self): # 프로젝트 전체 목록 얻어오기 2022-09-08 테스트 성공
        return self.jira.projects()

    @logging_deco
    def get_my_issue(self) -> list:
        """ 
        나(config.py의 myid)에게 할당된 이슈의 정보를 정리하여 반환함.

        Returns:
        - list_res : [[지난 날짜, 이슈 코드, 패치 일정, 고객사, 내용 요약, url], ...]
        """
        list_res = []
        for x in self.list_projects_key:
            q = f'project = "{x}" AND assignee = {self.myid} ORDER BY created DESC'
            try:
                for iss in self.jira.search_issues(q):
                    day = datetime.now() - datetime.strptime(iss.fields.created, '%Y-%m-%dT%H:%M:%S.%f%z').replace(tzinfo=None)
                    list_tmp = [day.days, iss.key, iss.fields.customfield_10172, iss.fields.customfield_10121, iss.fields.summary, config.jira_server + "/browse/" + iss.key]
                    
                    list_res.append(list_tmp)
            except:
                pass

        return list_res

if __name__ == '__main__':
    jira = Jira()
    mode = 1
    if mode == 1:
        """
        나에게 할당된 이슈 오래된 순서로 정렬해서 가져오기
        - 작성일 : 2022-09-15
        - 마지막 테스트 날짜 : 2022-10-31, 성공
        - 기능 사용 대상 : 
        - 기능 사용 가능 조건 : 
        - 사용 시 주의사항 : config.py의 token과 id 를 본인의 값으로 변경해주어야함.
        """
        cnt = 0
        file_path =  path.home_path + f"/Desktop/MyIssue_{jira.today_yyyymmdd}.txt" # 파일명, 경로 변경 필요 (날짜 넣기)
        list_result = list(reversed(sorted(jira.get_my_issue(), key=lambda x:x[0])))
        
        str_res = ""
        for str_tmp in list_result:
            str_res += str(str_tmp) + "\n"
            cnt+=1
        
        str_res_2 = ""
        for str_tmp in list_result:
            str_res_2 += str(str_tmp[1]) + "\n"
            cnt+=1
        
        print("count :" + str(cnt))

        with open(file_path, "w") as f:
            f.write(str_res)
            f.write(str_res_2)

    elif mode == 2: # 이슈 속성 얻어오기
        #q = 'project = "" ORDER BY created DESC'
        q = 'key = "H0123-0000"'
        issues = jira.jira.search_issues(q)
        for iss in issues:
            #o = jira.jira.issue(iss.key)
            print(iss)
            for i in dir(iss.fields):
                print(i, str(getattr(iss.fields, i)))
                #if "" == i:
                    #print(str(getattr(iss.fields, i)))
            #    if i == 'assignee' and "담당자" in str(getattr(iss.fields,i)):
            #        print(iss.key, " - " + iss.raw['fields'][i])
            #print(o.assignee)

        #iss = jira.jira.issue('이슈코드')
        #for i in dir(iss.fields):
        #    print(i+":"+str(getattr(iss.fields,i)))
    elif mode == 3:
        print(jira.get_my_issue())
    