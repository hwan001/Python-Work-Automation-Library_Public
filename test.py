
# Immutable : 숫자(number), 문자열(string), 튜플(tuple) -> 값 변경 불가.
# Mutable : 리스트(list), 딕셔너리(dictionary), NumPy의 배열(ndarray) -> 값 변경 가능
# 
# tmp = ''.join(map(str, [1, 2, 3, 4, 5, 6, 7]))
# print(tmp, type(tmp))
# 

import selenium
import path
import os

def get_deployInfo(target_path): # target_path 내부의 rpm 파일과 txt 파일명 가져오기
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

if __name__ == '__main__':

    for x in get_deployInfo("C:/FTC_downloads/releaseVersion_RPM/3.0.54"):
        print(x)