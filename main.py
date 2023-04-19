
import subprocess as subp
import os
import tkinter as tk
from tkinter import filedialog

import ocrmypdf

filename = None
file_path_full = None
# ToDo Set Up Logging

# ToDo Actually Comment the damn Code

# ToDo Make GUI Pretty
# ToDo Add Custom/Smart Language Selector

def select_file():
    global filename
    global file_path_full
    file_path_full = filedialog.askopenfilename(defaultextension=".pdf")
    filename = os.path.basename(file_path_full)
    print(filename)

def ocr_done(filepath):
    confirmation_window = tk.Toplevel()
    confirmation_window.wm_title("OCR Finished")

    label = tk.Label(confirmation_window, text=f"OCR is finished!")
    path  = tk.Label(confirmation_window, text=f"File saved at {filepath}")
    button_open_file = tk.Button(confirmation_window, text="Open File", command=lambda: os.startfile(filepath))
    button_open_folder  = tk.Button(confirmation_window, text="Open Folder", command=lambda: subp.run(f'Explorer.exe "{os.path.normpath(os.path.dirname(filepath))}"'))
    button_close_window = tk.Button(confirmation_window, text="Close", command=confirmation_window.destroy)

    label.grid(row=0, column=0)
    path.grid(row=1, column=0)
    button_open_file.grid(row=2, column=0)
    button_open_folder.grid(row=3, column=0)
    button_close_window.grid(row=3, column=1)

def redo_ocr_click(lang, output_file, input_file, win):
    ocr(lang=lang, input_file=input_file, output_file=output_file, force_ocr=True)
    win.destroy()




def ocr_found(lang_tmp, output_file, input_file):
    ocr_found_window = tk.Toplevel()
    ocr_found_window.wm_title("Prior OCR found!")

    l = tk.Label(ocr_found_window, text="File already has searchable Text")
    l.grid(row=0, column=0)

    l2 = tk.Label(ocr_found_window, text="Force OCR ? ")
    l2.grid(row=1, column=0)

    b1 = tk.Button(ocr_found_window, text="Force OCR", command=lambda: redo_ocr_click(lang_tmp, output_file, input_file, ocr_found_window), )
    b1.grid(row=2, column=0)

    b2 = tk.Button(ocr_found_window, text="Cancel", command=ocr_found_window.destroy)
    b2.grid(row=2, column=1)


def select_folder():
    global output_folder
    output_folder = filedialog.askdirectory()
    print(output_folder)


def ocr(lang, output_file, input_file, force_ocr=False):
    print(f'ocr with Lang={lang}')
    try:
        ocrmypdf.ocr(lang=lang, input_file=input_file, output_file=output_file, force_ocr=force_ocr)

    except ocrmypdf.PriorOcrFoundError:
        print(f"Prior OCR found ! lang: {lang} ")
        ocr_found(lang, output_file, input_file)
    ocr_done(output_file)

def confirm(lang: str):
    """
    starts OCR with the Selected File and Language

    :param lang: Str: Language String
    :return:
    """
    if filename:
        print(lang)
        ocr(lang, output_folder + '/' + filename, file_path_full)

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

    confirm_button = tk.Button(root, text="OCR starten", command=lambda: confirm(str(lang.get())))
    confirm_button.pack()
    root.mainloop()
