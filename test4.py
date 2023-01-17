dict_숫자 = {
    0:"",
    1:"일",
    2:"이",
    3:"삼",
    4:"사",
    5:"오",
    6:"육",
    7:"칠",
    8:"팔",
    9:"구",
}

dict_단위 = {
    1:"",
    10:"십",
    100:"백",
    1000:"천",
}

dict_자리수={
    0:"",
    1:"만",
    2:"억",
    3:"조",
    4:"경",
    5:"해",
    6:"자",
    7:"양",
    8:"구",
    9:"간",
    10:"정",
    11:"재",
    12:"극",
    13:"항하사",
    14:"아승지",
    15:"나유타",
    16:"불가사의",
    17:"무량대수",
    18:"겁",
    19:"업",
}

def test2(int_num):
    cnt = 0
    stack_tmp = []

    while int_num > 0:
        tmp = int_num%10000
        cnt_2 = 1
        list_tmp = []

        while tmp > 0:
            if not (tmp % 10 == 0):
                list_tmp.append(dict_단위[cnt_2])
            if not (tmp % 10 == 1 and (cnt_2 in [10, 100, 1000] or cnt == 1)):
                list_tmp.append(dict_숫자[tmp % 10])
            cnt_2 *= 10
            tmp //= 10
        
        stack_tmp.append("".join(list(reversed(list_tmp))) + dict_자리수[cnt] + " ")

        int_num //= 10000
        cnt += 1

    return "".join(list(reversed(stack_tmp)))



#for i in range(999, 1999, 1):
#    for j in range(10, 20, 1):
#        print(f"{test2(i)}({i}) * {test2(j)}({j}) = {test2(i*j)}({i*j})")

try:
    print(test2(12201327154061201304064198652502180290011123456245562054063034530450140304560005))
except:
    print("Out of bounds")