import PyPDF2
import os
from tkinter import messagebox, Tk

def merge_pdf(path, filename="combined"):
    """Simple function to merge pdf files. Can be run as standalone.
    Checks for valid path and uses default filename if not specified by user.
    Outputs merged file and messagebox with info about the result"""
    merger = PyPDF2.PdfMerger()

    if os.path.exists(path):
        count = 0
        for file in os.listdir(path):
            if file.endswith(".pdf"):
                count += 1
                full_path = os.path.join(path, file)
                merger.append(full_path)

        if filename == '':
            filename = "combined"

        filename = filename + '.pdf'
        output_path = os.path.join(path, filename)
        if count != 0:
            merger.write(output_path)
            messagebox.showinfo(title="PDF Merger", message=f"Success. Datei gespeichert unter {output_path}")
        else:
            messagebox.showwarning(title="PDF Merger", message="No files found to merge")

        merger.close()
    else:
        messagebox.showerror(title="PDF Merger", message="The specified path does not exist!")

if __name__ == "__main__":
    root = Tk()
    root.withdraw()

    merge_pdf(input("Enter a path: "), input("Enter a filename: "))

    root.destroy()