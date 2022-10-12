import sys
import subprocess

"""
try:
    import pyautogui
    import pyperclip
    import pywinauto

except:
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '-r', 'requirements.txt'])
"""
import pyautogui
import pywinauto

class Gui():
    def __init__(self):
        pass

    def connect_targetElements(self, target_process):
        app = pywinauto.application.Application(backend="uia")
        for proc in pywinauto.findwindows.find_elements():
            if proc.name == "*" + target_process + "*":
                break

        return app.connect(process = proc.process_id)


    def ctrl_a(self):
        pyautogui.hotkey('ctrl', 'a')

    def ctrl_c(self):
        pyautogui.hotkey('ctrl', 'c')

    def ctrl_v(self):
        pyautogui.hotkey('ctrl', 'v')

    def Quick_launch(self):
        pyautogui.hotkey('win', 'r')
    
    def create_notepad(self):
        self.Quick_launch()
        pyautogui.typewrite('notepad', interval=0.1)
        pyautogui.press('enter')
        
    def get_clipboard(self):
        pass
    
    def set_focus(self):
        pass 



def solution_tmp():
    import random
    #tmp = [99, 9, 999, 998, 981, 98, 101]
    tmp = list(set([random.randint(0, 1000) for _ in range(100)]))
    
    tmp_1=[]
    tmp_2=[]
    tmp_3=[]

    # 자리수 별 나누기
    for x in tmp:
        if x >= 100 and x < 1000:
            tmp_3.append(x)
        if x >= 10 and x < 100:
            tmp_2.append(x)
        if x >= 0 and x < 10:
            tmp_1.append(x)
        
    tmp_3 = list(reversed(sorted(tmp_3, key=lambda x:( str(x)[0], str(x)[1], str(x)[2] ) )))
    tmp_2 = list(reversed(sorted(tmp_2, key=lambda x:( str(x)[0], str(x)[1] ) )))
    tmp_1 = list(reversed(sorted(tmp_1, key=lambda x:( str(x)[0] ) )))
    
    print(tmp_3, tmp_2, tmp_1)


if __name__ == '__main__':
    #solution_tmp()
    my_gui = Gui()
    #my_gui.connect_targetElements("메모장").print_control_identifiers()
    
    #pyautogui.click(200, 100)
    #my_gui.ctrl_a()
    #my_gui.ctrl_c()

    #my_gui.create_notepad()
    #clip_text = pyperclip.paste()
    #print(clip_text)
    #print(pyautogui.position())
    #print(pyautogui.size())



