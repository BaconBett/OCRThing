import logging
import ocrmypdf
import os
import tkinter as tk
from tkinter import filedialog
filename = None
file_path_full = None

def select_file():
    global filename
    global file_path_full
    file_path_full = filedialog.askopenfilename(defaultextension=".pdf")
    filename = os.path.basename(file_path_full)
    print(filename)


def select_folder():
    global output_folder
    output_folder = filedialog.askdirectory()
    print(output_folder)


def ocr(lang, output_file, input_file):

    print(f'ocr mit Lang={lang}')
    try:
        ocrmypdf.ocr(lang=lang, input_file=input_file, output_file=output_file)

    except ocrmypdf.PriorOcrFoundError:

        # ToDo MessageBox "OCR bereits vorhanden",  wahl ob abbruch oder force_ocr
def confirm(lang: str):
    """
    startet OCR mit der Ausgewählten datei und sprache

    :param lang: Str: Sprache
    :return:
    """
    if filename:
        print(lang)
        ocr(lang, output_folder +'/'+ filename, file_path_full)

    else:
        print('hmm file')

    return


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("300x200")

    file_button = tk.Button(root, text="Select File", command=select_file)
    file_button.pack()
    output_folder_button = tk.Button(root, text="Zielordner", command=select_folder)
    output_folder_button.pack()

    lang = tk.StringVar(value="option2")

    option1 = tk.Radiobutton(root, text="DE", variable=lang, value="deu")
    option1.pack()
    option2 = tk.Radiobutton(root, text="EN", variable=lang, value="eng")
    option2.pack()
    option3 = tk.Radiobutton(root, text="ITA", variable=lang, value="ita")
    option3.pack()

    confirm_button = tk.Button(root, text="OCR starten", command=lambda: confirm(lang.get()))
    confirm_button.pack()
    root.mainloop()
