import os

# 경로
home_path = os.environ["USERPROFILE"]
file_path = "C:/tmp"
after_upload_path = file_path + "/업로드완료"
gdirve_path = "G:/tmp"
gdrive_path_version = "G:/tmp"
gdrive_patch_docx = "/tmp.docx"
test_desktop_path =  home_path + "/Desktop/test.docx"

# 배포 정보
dict_company = {
    "company_name":{"name":"company_name","url":"url"},
}