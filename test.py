
# Immutable : 숫자(number), 문자열(string), 튜플(tuple) -> 값 변경 불가.
# Mutable : 리스트(list), 딕셔너리(dictionary), NumPy의 배열(ndarray) -> 값 변경 가능
# 
# tmp = ''.join(map(str, [1, 2, 3, 4, 5, 6, 7]))
# print(tmp, type(tmp))
# 
# 구글 드라이브 경로 정리하기
import os
import path as path_my
from genericpath import isdir

def find_dir(path, str_space):
    for x in os.listdir(path):
        tmp = f"{path}/{x}".replace("//", "/")
        if isdir(tmp):
            print(str_space + x)
            find_dir(tmp, str_space + "  ")

def make_dir(path):
    for x in os.listdir(path):
        if ".ini" in x: continue
        if "기타" in x: continue

        tmp = f"{path}/{x}".replace("//", "/")
        if isdir(tmp):
            pass

def find_path():
    target_path = [path_my.gdrive_path_version]
    
    for tmp_path in target_path:
        print("\nstart : ", tmp_path) 
        make_dir(tmp_path, "")
        print("\nend : ", tmp_path) 

if __name__ == '__main__':
    find_dir(path_my.gdrive_path_version, "")

