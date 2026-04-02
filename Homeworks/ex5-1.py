import os

def find_pdf_size(top):
    pdf_size = 0
    pdf_no = 0
    for root, dirs, files in os.walk(top):
        for name in files:
            if name.lower().endswith('.pdf'):
                pdf_size += os.path.getsize(os.path.join(root, name))
                pdf_no += 1
    return [pdf_size, pdf_no] 

path = input("Enter top directory path: ")
size, number = find_pdf_size(path)
print(f'{number} PDF files consumes {size} bytes in entered directory tree.')

"""
Example:

Enter top directory path: C:\Users\pfili\Documents\STUDIA\ZAJECIA\s10\srst                                                                           
26 PDF files consumes 274484324 bytes in entered directory tree.
"""