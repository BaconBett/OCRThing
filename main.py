import subprocess as subp
import os
import tkinter as tk
from tkinter import filedialog

import ocrmypdf

filename = None
file_path_full = None
output_folder = None


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
    """
    Creates a Confirmation Window with the Option to Open either the .PDF itself
    or the Folder that it was saved in.
    :param filepath: Full path to the Finished .PDF
    """
    confirmation_window = tk.Toplevel()
    confirmation_window.wm_title("OCR Finished")

    filepath = os.path.normpath(os.path.dirname(filepath))

    label = tk.Label(confirmation_window, text=f"OCR is finished!")
    path = tk.Label(confirmation_window, text=f"File saved at {filepath}")

    # Button to open the processed file
    button_open_file = tk.Button(confirmation_window,
                                 text="Open File",
                                 command=lambda: os.startfile(filepath))

    # Button to open the folder in that the file was saved in
    button_open_folder = tk.Button(confirmation_window,
                                   text="Open Folder",
                                   command=lambda: subp.run(f'Explorer.exe "{filepath}"'))

    button_close_window = tk.Button(confirmation_window, text="Close", command=confirmation_window.destroy)

    # Assign positions
    label.grid(row=0, column=0)
    path.grid(row=1, column=0)
    button_open_file.grid(row=2, column=0)
    button_open_folder.grid(row=3, column=0)
    button_close_window.grid(row=3, column=1)


def redo_ocr_click(lang_temp, output_file, input_file, win):
    """
    Method to Restart the OCR Process and close an error window
    after it has been previously stopped due to an Exception
    :param lang_temp: 3 Char long Language String
    :param output_file: Name and Path of the Output .PDF
    :param input_file: Name and Path of the Input .PDF/Scanned Image
    :param win: tkinter Window object
    :return: none
    """

    try:
        ocr(lang_tmp=lang_temp, input_file=input_file, output_file=output_file, force_ocr=True)
    except ocrmypdf.exceptions as OcrException:
        print(OcrException)

    win.destroy()


def ocr_found(lang_tmp, output_file, input_file):
    ocr_found_window = tk.Toplevel()
    ocr_found_window.wm_title("Prior OCR found!")

    message_label = tk.Label(ocr_found_window, text="File already has searchable Text")
    message_label.grid(row=0, column=0)

    message_label_2 = tk.Label(ocr_found_window, text="Force OCR ? ")
    message_label_2.grid(row=1, column=0)

    force_ocr_button = tk.Button(ocr_found_window,
                                 text="Force OCR",
                                 command=lambda: redo_ocr_click(lang_tmp, output_file, input_file, ocr_found_window))

    force_ocr_button.grid(row=2, column=0)

    cancel_button = tk.Button(ocr_found_window,
                              text="Cancel",
                              command=ocr_found_window.destroy)

    cancel_button.grid(row=2, column=1)


def select_folder():
    global output_folder
    output_folder = filedialog.askdirectory()
    print(output_folder)


def ocr(lang_tmp, output_file, input_file, force_ocr=False):
    print(f'ocr with Lang={lang_tmp}')
    try:
        ocrmypdf.ocr(lang=lang_tmp, input_file=input_file, output_file=output_file, force_ocr=force_ocr)

    except ocrmypdf.PriorOcrFoundError:
        print(f"Prior OCR found ! lang: {lang_tmp} ")
        ocr_found(lang_tmp, output_file, input_file)
    ocr_done(output_file)


def confirm(lang_tmp: str):
    """
    starts OCR with the Selected File and Language

    :param lang_tmp: Str: Language String
    
    """
    if filename:
        print(lang_tmp)
        ocr(lang_tmp, f'{output_folder}' + '/' + f'{filename}', file_path_full)

    else:
        print('hmm file')


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("230x200")
    root.wm_title("OCR Tool")

    label1 = tk.Label(text="Please Select a .PDF ")
    label2 = tk.Label(text="and a Target Folder")
    label1.pack()
    label2.pack()

    file_button = tk.Button(root, text="Select File", command=select_file)
    file_button.pack()
    output_folder_button = tk.Button(root, text="Target Folder", command=select_folder)
    output_folder_button.pack()

    lang = tk.StringVar(value="option2")

    option1 = tk.Radiobutton(root, text="DE", variable=lang, value="deu")
    option1.pack()
    option2 = tk.Radiobutton(root, text="EN", variable=lang, value="eng")
    option2.pack()
    option3 = tk.Radiobutton(root, text="ITA", variable=lang, value="ita")
    option3.pack()

    confirm_button = tk.Button(root, text="Start OCR", command=lambda: confirm(str(lang.get())))
    confirm_button.pack()
    root.mainloop()
