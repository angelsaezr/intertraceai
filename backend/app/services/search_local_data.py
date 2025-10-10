import os

folder = r"C:\Users\angel\Downloads"
pdfs = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]

for pdf in pdfs:
    print(os.path.join(folder, pdf))
