import sys
import subprocess

try:
    import docx

except:
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '-r', 'requirements.txt'])

    import docx

import path

class Docx():
    def __init__(self):
        pass

    def append_contents(self, file_path, paragraph):
        doc = docx.Document()
        doc.add_paragraph(paragraph)
        doc.save(file_path)



if __name__ == '__main__':
    #my_doc = Docx()
    #my_doc.append_contents()
    pass