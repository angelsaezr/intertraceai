import os


# Search documents from os
class Engine:
    def __init__(self):
        self.folder = r"C:\Users\angel\Downloads"
        self.pdfs = [f for f in os.listdir(self.folder) if f.lower().endswith(".pdf")]

    def search(self, query):
        results = []
        for pdf in self.pdfs:
            if query.lower() in pdf.lower():
                results.append(os.path.join(self.folder, pdf))
        return results