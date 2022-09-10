from my_function import *


# 이스케이프 시퀀스
# = \u003d
# / %2F
#   \u0020

#str_version = input("version : ")
#str_company = input("version : ")

res = ""
alert = "!!!진행 전 해당 버전 마스터의 누락된 사항 확인하기!!!"
print (alert)


tmp = my_class("version", "site-code")

sel = 0
if sel == 1:
    tmp.Make_CompanyBranch_Details_Manual()
elif sel == 2:
    res = tmp.git_repo(True) # 2022-07-05 테스트 성공, 2022-09-05 정상 
elif sel == 3:
    tmp.my_jenkins_build() # 2022-09-05 테스트는 성공, 2022-09-07 정상 



# TEST
#ping()
# cd /home/qa/onenet_tmp/ ddddd  /log
# while true; do ls -al; sleep 3; clear; done;
#ssh_onenet_property_check("echo test")
#ssh_onenet_property_check("find_target onenet_ip 2> filename;cat filename;sleep 1;rm -rf filename")

#check_branchName("")

#test_file_create(b'1', "b") # 대용량 더미 txt 파일 생성 
#scan_CommitStatus1("open")
#download_CsvFile()python 

# TEST File
#from shutil import copyfile

#for i in range(1, 101):
#    copyfile("C:\\Users\\hjh\\Desktop\\aa\\10m.xlsx", "C:\\Users\\hjh\\Desktop\\aa\\10m_" + str(i) + ".xlsx")
