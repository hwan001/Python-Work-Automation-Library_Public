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

    def get_deployInfo(self, target_path): # target_path 내부의 rpm 파일과 txt 파일명 가져오기
        site_version = ""
        change_name = ""
        seperator_string = "-r" if "releaseVersion_RPM" in target_path else ".r"
        list_filepath = [] 

        for x in os.listdir(target_path):
            if ".rpm" in x:
                site_version += x.split(seperator_string)[0]+"\n"
                list_filepath.append(target_path + "/" + x)
            elif ".txt" in x:
                change_name = x

        return site_version, change_name, list_filepath

    def make_template(self, site_code, workspace): # RPM 배포 템플릿 생성하기
        # 사이트 명
        target = path.dict_company[site_code]["name"]
        download_link = path.dict_company[site_code]["url"]

        # 해당 경로 내부의 rpm 파일과 txt 파일명 가져오기
        site_version, change_name, _ = self.get_deployInfo(f"{workspace}/{site_code}")

        # txt 파일 내용 가져오기
        site_contents = ""
        txt_filename = f"{workspace}/{site_code}/{change_name}"
        #print(txt_filename)
        with open(txt_filename, "r", encoding="utf8") as file:
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
        jira_template = "*" + target + f"({site_code}) " if "/companyVersion_RPM" in workspace else " "
        jira_template += "RPM 배포*\n"
        jira_template += f"\n버전 : \n{site_version} \n" # get RPM으로 얻어와서 여러줄 추가
        jira_template += f"\n수정 내용 : \n{site_contents}\n" # get txt로 얻어와서 여러줄 추가
        jira_template += f"\n다운로드 경로 : \n{download_link}\n" # 업로드 경로가 다운로드 경로

        return jira_template, jira_issue_link

    @logging_deco
    def get_my_issue(self): # 나에게 할당된 이슈들 링크, 제목, 지난 날짜를 알려줌 -> 2022-09-08 성공
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

    def add_comment(self, issue_code, comment): # 특정 이슈에 댓글 달기 2022-09-08 테스트 성공
        comment_to_edit = self.jira.add_comment(issue_code, 'Change this content later')
        comment_to_edit.update(body=comment)

    def append_docx(self, file_name, contents): # docx에 수정 내용 이어붙이기
        my_docx = func_docx.Docx(file_name)
        my_docx.append_contents(contents)
    
    @logging_deco
    def upload_gdrive(self, site_code, workspace): # G-Drive 자동 업로드
        # 사이트 코드로 업로드할 드라이브 경로 찾기
        if "/companyVersion_RPM" in workspace:
            for x in os.listdir(path.gdirve_path):
                if site_code + "_" in x:
                    target_path = path.gdirve_path + "/" + x + "/패치"
                    break
        else:
            for x in os.listdir(path.gdrive_path_version):
                mid_path = ".".join(map(str, site_code.split(".")[:-1]))
                if mid_path in x:
                    target_path = path.gdrive_path_version + f"/V{mid_path}/{site_code}/패치"
                    break

        print(target_path)

        # 해당 경로 내부의 rpm 파일과 txt 파일명 가져오기
        source_path, change_name, list_filepath = self.get_deployInfo(f"{workspace}/{site_code}")
        #source_path = source_path.split("\n")[:-1]
        print(list_filepath, len(list_filepath))

        # 구글 드라이브 데스크탑으로 업로드하기
        for x in list_filepath:
            try:
                shutil.copy(x, target_path)
                print(x + " - 업로드 완료")
            except:
                print(x + " - 실패")

        # 업로드한 페이지 열기
        webbrowser.open(path.dict_company[site_code]["url"])

        # txt 파일 내용 가져오기
        site_contents = ""
        with open(workspace + "/" + site_code + "/" + change_name, "r", encoding="utf8") as file:
            for tmp in file.readlines():
                site_contents += tmp.replace("#", "")
        self.site_contents = site_contents

        # docx에 수정 내용 추가
        print("파일 명 : " + target_path + path.gdrive_patch_docx)
        self.append_docx(target_path + path.gdrive_patch_docx, self.site_contents + "\n")

    @logging_deco
    def auto_comment(self, site_code, white_list, workspace): # 템플릿 만들어서 JIRA 댓글 달기
        if path.dict_company[site_code]["url"] == "":
            print("다운로드 링크 없음")
            return "다운로드 링크 없음"

        if path.dict_company[site_code]["name"] == "":
            print("사이트명 없음")
            return "사이트명 없음"

        if site_code != "":
            str_template, issue_code_list = self.make_template(site_code, workspace)
        else:
            print("사이트 코드 없음")
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

    if mode == 1: # Company RPM 배포 자동화
        """
        # Company RPM 배포 자동화
        - 작성일 : 2022-09-15
        - 마지막 수정일 : 2022-11-07
        - 마지막 테스트 날짜 : 2022-11-04, 성공
        - 기능 사용 대상 :  컴퍼니 브랜치가 존재하는 사이트
        - 기능 사용 가능 조건 : workspace 위치에 컴퍼니 코드 형태의 폴더 내부에 'Gerrit 수정내용이 담긴 txt, 해당 rpm' 존재
        - 사용 시 주의사항 : 
            white_list 에 값이 "ALL" 이면 txt에서 검출된 모든 이슈코드에 댓글이 올라감. 
            일부만 필요시는 리스트에 직접 작성해주면됨.
            ex) white_list = ["H0000-0000", "H1234-1234"]
        """
        white_list = ["H0158-2547", "H0158-2368"]

        workspace = path.file_path + "/companyVersion_RPM"
        if not isdir(workspace):
            os.mkdir(workspace)
            print("No Files")
            sys.exit()

        site_codes = []
        for x in os.listdir(workspace):
            if isdir(workspace + "/" + x):
                site_codes.append(x)

        for site_code in site_codes:
            jira.make_template(site_code, workspace)

        for site_code in site_codes:
            jira.upload_gdrive(site_code, workspace)
            jira.auto_comment(site_code, white_list, workspace) 

    elif mode == 2: # 나에게 할당된 이슈 오래된 순서로 정렬해서 가져오기
        """
        # 나에게 할당된 이슈 오래된 순서로 정렬해서 가져오기
        - 작성일 : 2022-09-15
        - 마지막 테스트 날짜 : 2022-10-31, 성공
        - 기능 사용 대상 : 
        - 기능 사용 가능 조건 : 
        - 사용 시 주의사항 : config.py의 token과 id 를 본인의 값으로 변경해주어야함.
        """
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
    
    elif mode == 4: # [작성중] Release RPM 배포 자동화
        """
        # Release RPM 배포 자동화
        - 작성일 : 2022-11-04
        - 마지막 수정일 : 2022-11-07
        - 마지막 테스트 날짜 : 2022-11-07, x : 경로 문제로 파일 업로드 에러 -> 수정
        - 기능 사용 대상 :  릴리즈 버전 사용 사이트
        - 기능 사용 가능 조건 : workspace 위치에 버전명 형태의 폴더 > Gerrit 수정내용이 담긴 txt, 해당 rpm
        - 사용 시 주의사항 : 
            white_list 에 값이 "ALL" 이면 txt에서 검출된 모든 이슈코드에 댓글이 올라감. 
            일부만 필요시는 리스트에 직접 작성해주면됨.
            ex) white_list = ["H0000-0000", "H1234-1234"]
        """
        
        white_list = [""]
        workspace = path.file_path + "/releaseVersion_RPM"

        if not isdir(workspace):
            os.mkdir(workspace)
            print("No File")
            sys.exit()

        versions = []
        for x in os.listdir(workspace):
            if os.path.isdir(workspace + "/" + x):
                versions.append(x)
        
        for version in versions:
            jira.upload_gdrive(version, workspace)
            jira.auto_comment(version, white_list, workspace) 