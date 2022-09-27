from my_function import *
from pyparsing import empty


# 이스케이프 시퀀스
# = \u003d
# / %2F
#   \u0020

#str_version = input("version : ")
#str_company = input("version : ")

res = ""
alert = "!!!진행 전 해당 버전 마스터의 누락된 사항 확인하기!!!"
print (alert)


### TEST ###
# Create dummy file for TEST
def test_file_create(data, unit="gb"):
    dict_size = {
        "b":1,
        "kb":1024, 
        "mb":1024*1024, 
        "gb":1024*1024*1024, 
        "B":1,
        "KB":1024, 
        "MB":1024*1024, 
        "GB":1024*1024*1024, 
    }

    with open("test_" + str(len(data)) + unit + ".txt", "wb") as f:
        f.write(data * dict_size[unit])
    
    print("Write ", len(data) * dict_size[unit])

#test_file_create(b'1', "b") # 대용량 더미 txt 파일 생성 