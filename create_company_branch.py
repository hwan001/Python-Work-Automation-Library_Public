import os
import sys
import config
import paramiko
import json
import requests

class Gerrit():
    def __init__(self):
        pass

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

class Jenkins():
    def __init__(self):
        pass
    
    def build(self, project_name=""):
        query = f"curl -X POST {config.jenkins_server}/job/{project_name}/build --user {config.jenkins_user}:{config.jenkins_pw}"
        os.system(query)

class Ssh():
    def __init__(self):
        pass

    def ssh_cmd(ip, port, user, pw, cmds):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(ip, port, user, pw)

        stdin, stdout, stderr = ssh.exec_command(";".join(cmds))

        lines = stdout.read()
        res = ''.join(str(lines))

        return res

class my_class:
    def __init__(self, str_version, str_company):
        #list_onenet_project_file = ["", "", "", ""]

        # gerrit에서 구분자가 다른 버전들 목록을 얻어옴
        gerrit = Gerrit()
        list_hyphen_version = []
        json_tmp = gerrit.send_api("/projects/onenet%2Frpm/branches", "GET")

        for tmp in json_tmp:
            try:
                str_tmp = tmp['ref'].split("release-")[1]
                if "-" not in str_tmp:
                    list_hyphen_version.append(str_tmp)
            except:
                pass
        
        #입력받은 버전이 위에서 얻어온 버전에 해당되면 구분자를 변경
        str_separator = "/"
        if str_version in list_hyphen_version:
            str_separator = "-"
                
        # 변수 설정        
        self.str_version = str_version 
        self.str_company = str_company
        
        self.urls = config.my_urls
        self.accounts = config.my_accounts

        # repo server info
        self.repo_ip = config.my_repo_ip
        self.repo_port = config.my_repo_port
        self.repo_user = config.my_repo_user
        self.repo_pw = config.my_repo_pw
    
        # gerrit var
        str_gerrit = str_version + "-" + str_company
        str_gerrit_branch = "release" + str_separator + str_gerrit
        str_gerrit_branch_2 = "release" + str_separator + str_version
        str_gerrit_manifest_comment = "[onenet][manifest] " + str_gerrit_branch_2 + " -> " + str_gerrit_branch + " revision 변경"
        str_gerrit_system_comment = "[onenet][system] " + str_gerrit_branch + " 생성 후 CONFIG_COMPANY_NAME 변경 : " + str_company
    
        # jenkins var
        str_jenkins = "name_v" + str_gerrit
        str_jenkins_2 = "name_v" + str_version
        
        # 아래 내용은 낮은 버전에서 변경되는 경우가 있음.
        self.list_jenkins_build_text = [
            #"export LANG=en_US.utf8",
            #"",
            #"#repo sync",
            "#repo start " + str_gerrit_branch + " --all",
            #"#repo forall -c \"git pull\"",
            #"",
            #"cd ${WORKSPACE}/onenet; ./config.sh -r rpm",
            #"sudo make -C ${WORKSPACE}/onenet clean",
            #"sudo make -C ${WORKSPACE}/onenet all install"
        ]

        self.list_repo_code = [
            "cd /home/qa",
            "mkdir test_tmp",
            "cd test_tmp",
            "mkdir " + str_gerrit,
            "cd " + str_gerrit,
            "mkdir log",
            f"repo init -u ssh://{config.jenkins_ssh}/test/manifest -m release.xml -b " + str_gerrit_branch_2 + " | tee -a log/repo_1.log",
            "repo sync | tee -a log/repo_2.log",
            "repo start " + str_gerrit_branch_2 + " --all | tee -a log/repo_3.log",
            "repo branch | tee -a log/repo_4.log",
            "repo sync | tee -a log/repo_5.log",
            "repo start " + str_gerrit_branch + " --all | tee -a log/repo_6.log",
            "repo branch | tee -a log/repo_7.log",
            "repo forall -c 'git push origin " + str_gerrit_branch + "' | tee -a log/repo_8.log",
            "echo !!fin!!"
        ]
        
        self.str_gerrit = str_gerrit
        self.str_gerrit_branch = str_gerrit_branch
        self.str_gerrit_branch_2 = str_gerrit_branch_2
        self.str_gerrit_manifest_comment = str_gerrit_manifest_comment
        self.str_gerrit_system_comment = str_gerrit_system_comment
        self.str_jenkins = str_jenkins
        self.str_jenkins_2 = str_jenkins_2
        
    # Create Company Bransh
    def Make_CompanyBranch_Details_Manual(self, isPrint=False, makeTxt=False):
        str_result = ""
        list_result = []
        debug = False
        file_path = os.environ["USERPROFILE"] + "/desktop/" + self.str_version + "-" + self.str_company + ".txt"
        
        str_result = "!!!진행 전 해당 버전 마스터의 누락된 사항 확인하기!!!"
        list_result.append(str_result)
        if debug: print(str_result)
        
        str_result = "---------------------------------------------------------"
        list_result.append(str_result)
        if debug: print(str_result)
        
        str_result = "Version : " + self.str_version
        list_result.append(str_result)
        if debug: print(str_result)
        
        str_result = "Company : " + self.str_company
        list_result.append(str_result)
        if debug: print(str_result)
        
        str_result = "\n1. Create Branch : " + self.urls[0]
        list_result.append(str_result)
        if debug: print(str_result)
        
        str_result = f" ID : {config.jenkins_user}"
        list_result.append(str_result)
        if debug: print(str_result)
        
        str_result = " PW : " + self.accounts[f"{config.jenkins_user}"]
        list_result.append(str_result)
        if debug: print(str_result)
        
        str_result = " Branch Name : " + self.str_gerrit_branch
        list_result.append(str_result)
        if debug: print(str_result)
        
        str_result = " Initial Revision : " + self.str_gerrit_branch_2
        list_result.append(str_result)
        if debug: print(str_result)
        
        str_result = "\n2. Create Change (onenet/manifest) : " + self.urls[1]
        list_result.append(str_result)
        if debug: print(str_result)
        
        str_result = " Select branch for new change : " + self.str_gerrit_branch
        list_result.append(str_result)
        if debug: print(str_result)
        
        str_result = " Description : " + self.str_gerrit_manifest_comment
        list_result.append(str_result)
        if debug: print(str_result)
        
        str_result = "\n default.xml :"
        str_default = '''<default revision="''' + self.str_gerrit_branch + '''" remote="origin"/>'''
        list_result.append(str_result)
        list_result.append(str_default)
        if debug: print(str_result)
        if debug: print(str_default)
        
        str_result = "\n release.xml :"
        str_release = '''<default revision="''' + self.str_gerrit_branch + '''" remote="origin"/>'''
        list_result.append(str_result)
        list_result.append(str_release)
        if debug: print(str_result)
        if debug: print(str_release)

        str_result = "\n\n3. Code-Review"
        list_result.append(str_result)
        if debug: print(str_result)
        
        str_result = f"\n\n4. New-Item_Jenkins: {self.urls[3]}"
        list_result.append(str_result)
        if debug: print(str_result)

        str_result = f" ID : {config.jenkins_user}"
        list_result.append(str_result)
        if debug: print(str_result)
        
        str_result = " PW : " + str(self.accounts[f"{config.jenkins_user}"])
        list_result.append(str_result)
        if debug: print(str_result)
        
        str_result = f" Enter an item name : {self.str_jenkins}"
        list_result.append(str_result)
        if debug: print(str_result)
        
        str_result = f" Copy from : {self.str_jenkins_2}"
        list_result.append(str_result)
        if debug: print(str_result)
        
        str_result = f" Manifest Branch : {self.str_gerrit_branch}"
        list_result.append(str_result)
        if debug: print(str_result)
        
        str_result = " Build > Execute shell : "
        list_result.append(str_result)
        if debug: print(str_result)
        
        for tmp in self.list_jenkins_build_text:
            list_result.append(tmp)
            if debug: print(tmp)
        
        
        str_result = f"\n\n5. Repo : {self.urls[4]}\ngit_repo 함수 활용 (수동 실행 시 아래 Command 참고)"
        list_result.append(str_result)
        if debug: print(str_result)
        
        # repo 
        str_result = " Command : "
        list_result.append(str_result)
        if debug: print(str_result)
        
        for cmd in self.list_repo_code:
            list_result.append(cmd)
            if debug: print(cmd)
        
        str_result = f"\n\n6. Create Change (onenet/system) : {self.urls[2]}"
        list_result.append(str_result)
        if debug: print(str_result)

        str_result = f" Select branch for new change : {self.str_gerrit_branch}"
        list_result.append(str_result)
        if debug: print(str_result)

        str_result = f" Description : {self.str_gerrit_system_comment}"
        list_result.append(str_result)
        if debug: print(str_result)
        
        str_result = " File : config/rpm/config.top"
        list_result.append(str_result)
        if debug: print(str_result)
        
        str_result = f" Edit : CONFIG_COMPANY_NAME=\"{self.str_company}\""
        list_result.append(str_result)
        if debug: print(str_result)
        
        str_result = "\n\n7. Code-Review"
        list_result.append(str_result)
        if debug: print(str_result)
        
        str_result = "\n\n8. Jenkins Build"
        list_result.append(str_result)
        if debug: print(str_result)
        
        str_result = "---------------------------------------------------------"
        list_result.append(str_result)
        if debug: print(str_result)
        
        if isPrint:
            for x in list_result:
                print(x)
        
        if makeTxt:
            for i in range(len(list_result)):
                list_result[i] += "\n"
                
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(list_result)
        
    # repo
    def git_repo(self, is_log=True):
        if is_log: print("Commands : ", ";".join(self.list_repo_code))
        return Ssh.ssh_cmd(self.repo_ip, self.repo_port, self.repo_user, self.repo_pw, self.list_repo_code)
    
    # build
    def jenkins_build(self):
        jenkins = Jenkins()
        jenkins.build(project_name=self.str_jenkins)
        
    
if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: python create_company_branch.py function_number")
        exit()
    
    list_target = []
    file_path = os.environ["USERPROFILE"] + "/desktop/create_company_branch.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        for tmp in f.readlines():
            if "pass" in tmp:
                continue
            tmp = tmp.replace("\n", "")
            tmp_split = tmp.split("-")
            list_target.append([tmp_split[0], tmp_split[1]])
    
    for target in list_target:
        tmp = my_class(target[0], target[1])

        sel = int(sys.argv[1])
        if sel == 1:
            tmp.Make_CompanyBranch_Details_Manual(isPrint=False, makeTxt=True)
        elif sel == 2:
            res = tmp.git_repo(True)
        elif sel == 3:
            tmp.jenkins_build()

        del tmp