import os
import re
from tkinter import Tk, messagebox

import PyPDF2


def sorted_nicely(file_list):
    """Sorts file names numerically if possible, otherwise alphabetically."""

    def alphanum_key(key):
        return [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", key)]

    return sorted(file_list, key=alphanum_key)


def merge_pdf(path, filename="combined"):
    """Merges PDF files in the specified directory in a sorted order."""
    merger = PyPDF2.PdfMerger()

    if os.path.exists(path):
        pdf_files = [file for file in os.listdir(path) if file.endswith(".pdf")]
        pdf_files = sorted_nicely(pdf_files)  # Sort alphabetically and numerically

        if pdf_files:
            for file in pdf_files:
                full_path = os.path.join(path, file)
                merger.append(full_path)

            filename = filename.strip() or "combined"
            output_path = os.path.join(path, filename + ".pdf")
            merger.write(output_path)
            merger.close()

            messagebox.showinfo(
                title="PDF Merger", message=f"Success. Datei gespeichert unter {output_path}"
            )
        else:
            messagebox.showwarning(title="PDF Merger", message="No PDF files found to merge")
    else:
        messagebox.showerror(title="PDF Merger", message="The specified path does not exist!")


if __name__ == "__main__":
    root = Tk()
    root.withdraw()

    merge_pdf(input("Enter a path: "), input("Enter a filename: "))

    root.destroy()
