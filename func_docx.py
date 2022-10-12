import sys
import subprocess

try:
    import docx

except:
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '-r', 'requirements.txt'])

    import docx
from datetime import datetime

import path

class Docx():
    def __init__(self, file_path):
        self.file_path = file_path

    def append_contents_1(self, file_path, paragraph):
        try:
            doc = docx.Document(file_path)
        except:
            doc = docx.Document()
            doc.save(file_path)
            doc = docx.Document(file_path)

        for p in doc.paragraphs: 
            print(p.text)

        doc.add_paragraph(paragraph)
        doc.save(file_path)

    def append_contents(self, paragraph):
        try:
            doc = docx.Document(self.file_path)
        except:
            doc = docx.Document()
            doc.save(self.file_path)
            doc = docx.Document(self.file_path)

        doc.add_paragraph().add_run("\n" + datetime.now().strftime('%Y-%m-%d')).bold = True
        doc.add_paragraph(paragraph)

        doc.save(self.file_path)

if __name__ == '__main__':
    my_doc = Docx("C:/Users/hwan/Desktop/test.docx")
    #my_doc.append_contents("C:/Users/hwan/Desktop/test.docx", datetime.now().strftime('%Y-%m-%d') + " test\n")
    #my_doc.append_contents_test("test2\n")

    pass