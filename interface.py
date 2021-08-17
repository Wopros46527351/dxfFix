from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd
 
def insert_text():
    global name  
    file_name = fd.askopenfilename()
    f = open(file_name)
    s = f.read()
    f.close()
    name.set(file_name)

    

 
root = Tk()
root.title("Open file")
 
name = StringVar()

 
name_label = Label(text="Введите название файла:")

 
name_label.grid(row=0, column=0, sticky="w")

 
name_entry = Entry(textvariable=name)

 
name_entry.grid(row=0,column=1, padx=5, pady=5)

 
 
message_button = Button(text="Open", command=insert_text)
message_button.grid(row=2,column=1, padx=5, pady=5, sticky="e")
 
root.mainloop()