import os
import re
from tkinter import Tk, messagebox

from pypdf import PdfReader, PdfWriter


def sorted_nicely(file_list):
    """Sorts file names numerically if possible, otherwise alphabetically."""

    def alphanum_key(key):
        return [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", key)]

    return sorted(file_list, key=alphanum_key)


def merge_pdf(path, filename="combined"):
    """Merges PDF files in the specified directory in a sorted order."""
    if not os.path.exists(path):
        messagebox.showerror(title="PDF Merger", message="The specified path does not exist!")
        return

    # Alle PDFs im Verzeichnis finden und sortieren
    pdf_files = [f for f in os.listdir(path) if f.lower().endswith(".pdf")]
    pdf_files = sorted_nicely(pdf_files)

    if not pdf_files:
        messagebox.showwarning(title="PDF Merger", message="No PDF files found to merge")
        return

    writer = PdfWriter()

    # Seiten aus jeder Datei hinzufügen
    for pdf in pdf_files:
        full_path = os.path.join(path, pdf)
        reader = PdfReader(full_path)
        for page in reader.pages:
            writer.add_page(page)

    # Ausgabedatei schreiben
    filename = filename.strip() or "combined"
    output_path = os.path.join(path, filename + ".pdf")
    with open(output_path, "wb") as out_f:
        writer.write(out_f)

    messagebox.showinfo(
        title="PDF Merger", message=f"Success. Datei gespeichert unter {output_path}"
    )


if __name__ == "__main__":
    root = Tk()
    root.withdraw()

    merge_pdf(input("Enter a path: "), input("Enter a filename: "))

    root.destroy()
