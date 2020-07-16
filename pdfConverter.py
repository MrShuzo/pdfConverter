import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import font
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import webbrowser
import pathlib

root_main = Tk()
root_merge = None
root_encrypt = None
image_merge = PhotoImage(file = str(pathlib.Path().absolute()) + "\images\merge.png")
image_encrypt = PhotoImage(file = str(pathlib.Path().absolute()) + "\images\encrypt.png")
image_folder = PhotoImage(file = str(pathlib.Path().absolute()) + "\images\open.png")

def mainGUI():
	root_main.title('PDF-Editor')
	root_main.geometry("300x160")
	root_main.resizable(False, False)
	information_text = Label(root_main, text="Choose an option")
	information_text.pack(side=TOP)
	creator_text = Label(root_main, text="Created by MrShuzo", fg="blue")
	f = font.Font(creator_text, creator_text.cget("font"))
	f.configure(underline=True)
	creator_text.configure(font=f)
	creator_text.bind("<Button-1>", open_github)
	creator_text.pack(side=BOTTOM)
	mergeButton = Button(root_main, command=lambda: mergeGUI(), height=130, width=150, image = image_merge, bg="#AD4E00", activebackground="#DB6200")
	mergeButton.pack(side=LEFT)
	encryptButton = Button(root_main, command=lambda: encryptGUI(), height=130, width=150, image = image_encrypt, bg="#62809E", activebackground="#89B2DD")
	encryptButton.pack(side=RIGHT)
	root_main.mainloop()

def encryptGUI():
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
	b = Button(root_encrypt, command=lambda: encrypt_pdfs(password_input.get()), height=70, width=130, image = image_folder, bg="#378dae", activebackground="#3d9dc2")
	b.pack(pady=2)
	root_encrypt.mainloop()

def mergeGUI():
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
	b = Button(root_merge, command=lambda: merge_pdfs(name_input.get() + ".pdf"), height=70, width=130, image = image_folder, bg="#378dae", activebackground="#3d9dc2")
	b.pack(pady=2)
	root_merge.mainloop()

output = Label(root_main, text="", fg="white")

def merge_pdfs(result_name):
	try:
		if result_name == ".pdf":
			change_btn("No name entered!", "red")
			return
		pdf_writer = PdfFileWriter()
		files = filedialog.askopenfilenames(parent=root_merge, title="Choose PDF-files", filetypes = [("PDF files", "*.pdf")])
		
		for file in root_merge.tk.splitlist(files):
			pdf_reader = PdfFileReader(file)
			for page in range(pdf_reader.getNumPages()):
				pdf_writer.addPage(pdf_reader.getPage(page))
		
		with open(result_name, 'wb') as out:
			if pdf_reader.getNumPages() != 0:
				change_btn("Successfully merged to " + result_name + "!", "green")
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
		filename = filedialog.askopenfilename(parent=root_encrypt, title="Choose PDF-file", filetypes = [("PDF files", "*.pdf")])
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

def change_btn(output_text, colour):
	output['text'] = output_text
	output['fg'] = colour
	output.pack(side=BOTTOM)

def open_github(event):
	webbrowser.open("https://github.com/MrShuzo")

mainGUI()