from func_jira import Jira

# 데코레이터 만들거
# 함수의 실행을 막는 데코레이터 (작성중, 테스트 모드일때만 작동)
# 함수의 실행 시간을 측정하는 데코레이터
# 로그용 데코

if __name__ == '__main__':
    jira = Jira()

    for str_tmp in jira.get_my_issue():
        print(str_tmp)
