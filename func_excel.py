import sys
import subprocess

try:
    import pyexcel

except:
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '-r', 'requirements.txt'])

    import pyexcel

import path

class Excel():
    def __init__(self):
        pass
    
    def test_sheet(self):
        sheet = pyexcel.Sheet()
        sheet.name = "name"
        sheet.ndjson = """
        {"year": ["2017", "2018", "2019", "2020", "2021"]}
        {"user": [129, 253, 304, 403, 545]}
        {"visit": [203, 403, 632, 832, 1023]}
        """.strip()

        print(sheet)

if __name__ == '__main__':
    #excel = Excel() 
    #excel.test_sheet()
    letter=[1, 2, 3]
    a = 1
    b = 2
    if 3 in [letter[2]]:
        a=b
    print(a)
    pass