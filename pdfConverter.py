import os
import pathlib
import webbrowser
from tkinter import *
from tkinter import filedialog, Label
from tkinter import font

from PyPDF2 import PdfFileReader, PdfFileWriter

root_main = Tk()
root_merge = None
root_encrypt = None
root_split = None
image_merge = PhotoImage(file=str(pathlib.Path().absolute()) + "\images\merge.png")
image_encrypt = PhotoImage(file=str(pathlib.Path().absolute()) + "\images\encrypt.png")
image_folder = PhotoImage(file=str(pathlib.Path().absolute()) + "\images\open.png")
image_split = PhotoImage(file=str(pathlib.Path().absolute()) + "\images\split.png")


def main_gui():
    root_main.title('PDF-Editor')
    root_main.geometry("468x200")
    root_main.resizable(False, False)
    information_text = Label(root_main, text="Choose an option")
    information_text.pack(side=TOP)
    creator_text = Label(root_main, text="Created by MrShuzo", fg="blue")
    f = font.Font(creator_text, creator_text.cget("font"))
    f.configure(underline=True)
    creator_text.configure(font=f)
    creator_text.bind("<Button-1>", open_github)
    creator_text.pack(side=BOTTOM)
    merge_button = Button(root_main, command=lambda: merge_gui(), height=130, width=150, image=image_merge,
                          bg="#AD4E00",
                          activebackground="#DB6200")
    merge_button.pack(side=LEFT)
    encrypt_button = Button(root_main, command=lambda: encrypt_gui(), height=130, width=150, image=image_encrypt,
                            bg="#62809E", activebackground="#89B2DD")
    encrypt_button.pack(side=RIGHT)
    split_button = Button(root_main, command=lambda: split_gui(), height=130, width=150, image=image_split,
                          bg="#4c6e3a",
                          activebackground="#79ab5f")
    split_button.pack(side=RIGHT)
    root_main.mainloop()


def encrypt_gui():
    global root_encrypt
    global output
    root_encrypt = Toplevel()
    output = Label(root_encrypt, text="", fg="white")
    root_encrypt.title('Encrypt')
    root_encrypt.geometry("210x150")
    root_encrypt.resizable(False, False)
    information_text = Label(root_encrypt, text="Password")
    information_text.pack(side=TOP)
    password_input = Entry(root_encrypt, bd=5)
    password_input.pack(side=TOP)
    b = Button(root_encrypt, command=lambda: encrypt_pdfs(password_input.get()), height=70, width=130,
               image=image_folder, bg="#378dae", activebackground="#3d9dc2")
    b.pack(pady=2)
    root_encrypt.mainloop()


def merge_gui():
    global root_merge
    global output
    root_merge = Toplevel()
    output = Label(root_merge, text="", fg="white")
    root_merge.title('Merge')
    root_merge.geometry("210x150")
    root_merge.resizable(False, False)
    information_text = Label(root_merge, text="Name Output-File")
    information_text.pack(side=TOP)
    name_input = Entry(root_merge, bd=5)
    name_input.pack(side=TOP)
    b = Button(root_merge, command=lambda: merge_pdfs(name_input.get() + ".pdf"), height=70, width=130,
               image=image_folder, bg="#378dae", activebackground="#3d9dc2")
    b.pack(pady=2)
    root_merge.mainloop()


def split_gui():
    global root_split
    global output
    root_split = Toplevel()
    output = Label(root_split, text="", fg="white")
    root_split.title('Split')
    root_split.geometry("250x200")
    root_split.resizable(False, False)
    name_text = Label(root_split, text="Name Output-File")
    name_text.pack(side=TOP)
    name_input = Entry(root_split, bd=5)
    name_input.pack(side=TOP)
    pages_text = Label(root_split, text="Page Numbers (i.e. 1, 2, 4)")
    pages_text.pack(side=TOP)
    pages_input = Entry(root_split, bd=5)
    pages_input.pack(side=TOP)
    b = Button(root_split, command=lambda: split_pdfs(name_input.get() + ".pdf", pages_input.get()), height=70,
               width=130,
               image=image_folder, bg="#378dae", activebackground="#3d9dc2")
    b.pack(pady=2)
    root_split.mainloop()


output = Label(root_main, text="", fg="white")


def merge_pdfs(result_name):
    global pdf_reader
    try:
        if result_name == ".pdf":
            change_btn("No name entered!", "red")
            return
        pdf_writer = PdfFileWriter()
        files = filedialog.askopenfilenames(parent=root_merge, title="Choose PDF-files",
                                            filetypes=[("PDF files", "*.pdf")])

        for file in root_merge.splitlist(files):
            pdf_reader = PdfFileReader(file)
            for page in range(pdf_reader.getNumPages()):
                pdf_writer.addPage(pdf_reader.getPage(page))

        with open(result_name, 'wb') as out:
            if pdf_reader.getNumPages() != 0:
                change_btn("Successfully merged to %s !" % result_name, "green")
            else:
                change_btn("No files selected!", "red")
            pdf_writer.write(out)
    except:
        change_btn("No files selected!", "red")
        os.remove(result_name)


def encrypt_pdfs(user_password):
    try:
        if user_password == "":
            change_btn("No password entered!", "red")
            return
        filename = filedialog.askopenfilename(parent=root_encrypt, title="Choose PDF-file",
                                              filetypes=[("PDF files", "*.pdf")])
        pdf_reader = PdfFileReader(filename)
        pdf_writer = PdfFileWriter()

        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))

        pdf_writer.encrypt(user_pwd=user_password, use_128bit=True)

        with open(filename[:-4] + ".encrypted.pdf", "wb") as out:
            if pdf_reader.getNumPages() != 0:
                change_btn("The file has been encrypted!", "green")
            else:
                change_btn("No file selected!", "red")
            pdf_writer.write(out)
    except:
        change_btn("No file selected!", "red")
        os.remove(user_password)


def split_pdfs(result_name, pages):
    try:
        if result_name == "" or pages == "":
            change_btn("No name or page numbers entered!", "red")
            return
        result_pages = [int(i) for i in pages.split(",")]
        filename = filedialog.askopenfilename(parent=root_split, title="Choose PDF-file", filetypes=[("PDF files", "*.pdf")])

        pdf_reader = PdfFileReader(filename)
        pdf_writer = PdfFileWriter()

        for page in result_pages:
            pdf_writer.addPage(pdf_reader.getPage(page-1))

        with open(result_name, 'wb') as out:
            if pdf_reader.getNumPages() != 0:
                change_btn("Successfully split to %s !" % result_name, "green")
            else:
                change_btn("No files selected!", "red")
            pdf_writer.write(out)
    except:
        change_btn("No file selected!", "red")
        os.remove(pages)
        os.remove(result_name)


def change_btn(output_text, colour):
    output['text'] = output_text
    output['fg'] = colour
    output.pack(side=BOTTOM)


def open_github(event):
    webbrowser.open("https://github.com/MrShuzo")


main_gui()