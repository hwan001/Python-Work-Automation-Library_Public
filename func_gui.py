import sys
import subprocess

try:
    import pyautogui
    import pyperclip
    import pywinauto

except:
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '-r', 'requirements.txt'])
    

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


if __name__ == '__main__':
    #my_gui = Gui()
    #my_gui.connect_targetElements("메모장").print_control_identifiers()
    
    tmp = [99, 9, 999, 998, 981, 98, 101]
    print(list(reversed(sorted(tmp, key=lambda x:(str(x)[0])))))

    #pyautogui.click(200, 100)
    #my_gui.ctrl_a()
    #my_gui.ctrl_c()

    #my_gui.create_notepad()
    #clip_text = pyperclip.paste()
    #print(clip_text)
    #print(pyautogui.position())
    #print(pyautogui.size())