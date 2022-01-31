from argparse import FileType
from cgitb import text
from distutils import command
from tkinter import *
from tkinter import filedialog, font

root = Tk()
root.title('NotePy')
root.geometry("800x500")

# Set de variável GLOBAL se arquivo tiver nome
global open_status_name
open_status_name = False

# Set de variável GLOBAL para texto selecionado
global selected
selected = False

# Funções do "MENU FILE"
# Comando "NEW FILE"
def new_file():
    # Limpar a tela de texto primeiro
    my_text.delete("1.0", END)
    # Alterar barra de status
    root.title('New File - NotePy')
    status_bar.config(text="New File   ")
    global open_status_name
    open_status_name = False

# Comando "OPEN FILE"    
def open_file():
    # Limpar a tela de texto primeiro
    my_text.delete(1.0, END)
    # Pegar o nome do Arquivo
    text_file = filedialog.askopenfilename(initialdir='/Users/marceloassim/Documents',
                                        title='Open File', 
                                        filetypes=(("Text Files", "*.txt"),
                                                    ("HTML Files", "*.html"), 
                                                    ("Python Files", "*.py"),
                                                    ("All Files", "*.*")))
    
    # Testar se há um nome de arquivo
    if text_file:
        # Se SIM, tornar o nome do arquivo GLOBAL
        global open_status_name
        open_status_name = text_file
    
    name= text_file    
    # Alterando o Status Bar
    status_bar.config(text=f'{name}')
    name.replace('/Users/marceloassim/Documents', '')
    root.title(f'{name} - NotePy')
    
    # Abrindo o arquivo
    text_file = open(text_file,'r')
    stuff = text_file.read()
    # Adicionando arquivo no textbox
    my_text.insert(END, stuff)
    # Fechando o arquivo
    text_file.close()

# Menu "SAVE AS"
def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension=".*",
                                            initialdir='/Users/marceloassim/Documents',
                                            title="Save As File", 
                                            filetypes=(("Text Files", "*.txt"),
                                                        ("HTML Files", "*.html"), 
                                                        ("Python Files", "*.py"),
                                                        ("All Files", "*.*")))
    if text_file:
        name= text_file
        status_bar.config(text=f'Saved: {name}')
        name.replace('/Users/marceloassim/Documents', '')
        root.title(f'{name} - NotePy')
        # Salvar o arquivo
        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0, END))
        # Fechando o arquivo
        text_file.close()

# Menu "SALVE"
def save_file():
    global open_status_name
    if open_status_name:
        # Salvar o arquivo
        text_file = open(open_status_name, 'w')
        text_file.write(my_text.get(1.0, END))
        # Fechando o arquivo
        text_file.close()
        # Alterar Barra de STATUS
        status_bar.config(text=f'Saved: {open_status_name}')
    else:
        save_as_file()

# FUNÇÕES DO "MENU EDIT"
# Menu "CUTE"
def cut_text(e):
    global selected
    # Check se utilizamos o atalho de teclado
    if e:
        selected = root.clipboard_get()
    else: 
        if my_text.selection_get():
            # pegar o texto selecionado
            selected = my_text.selection_get()
            # apagar o texto selecionado
            my_text.delete("sel.first", "sel.last")
            # Limpar a área de transferencia 
            root.clipboard_clear()
            root.clipboard_append(selected)

# Menu "COPY"
def copy_text(e):
    global selected
    # Check se utilizamos o atalho de teclado
    if e:
        selected = root.clipboard_get()
    else: 
        if my_text.selection_get():
            # pegar o texto selecionado
            selected = my_text.selection_get()
            # Limpar a área de transferencia 
            root.clipboard_clear()
            root.clipboard_append(selected)

# Menu "PASTE"
def paste_text(e):
    global selected
    # Check se utilizamos o atalho de teclado
    if e:
        selected = root.clipboard_get()
    else:
        if selected:
            position = my_text.index(INSERT)
            my_text.insert(position, selected)



# Criar "Interface Principal"
my_frame = Frame(root)
my_frame.pack(pady=5)

# Craiar "Barra de Rolagem"
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

# Criar "Área de Texto"
my_text = Text(my_frame, width=97, 
            height=25, 
            font=("Arial", 16),
            selectbackground="yellow", 
            selectforeground="black", 
            undo=True,
            yscrollcommand=text_scroll.set)
my_text.pack()

# Configurar "Barra de Rolagem"
text_scroll.config(command=my_text.yview)

# Criar "Menu"
my_menu = Menu(root)
root.config(menu=my_menu)

# Menu "FILE"
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file, accelerator="Command+N")
file_menu.add_command(label="Open", command=open_file, accelerator="Command+O")
file_menu.add_command(label="Save", command=save_file, accelerator="Command+S")
file_menu.add_command(label="Save As     ",command=save_as_file, accelerator="Command+Shit+S")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit, accelerator="Command+X")

# Menu "EDIT"
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=lambda: cut_text(False), accelerator="Command+X")
edit_menu.add_command(label="Copy", command=lambda: copy_text(False), accelerator="Command+C")
edit_menu.add_command(label="Past        ", command=lambda: paste_text(False), accelerator="Command+V")
edit_menu.add_separator()
edit_menu.add_command(label="Undo", command=my_text.edit_undo, accelerator="Command+Z")
edit_menu.add_command(label="Redo", command=my_text.edit_redo, accelerator="Command+Y")

# Criar "Status Bar"
status_bar = Label(root, text='.: Pronto :.')
status_bar.pack(fill=X, side=BOTTOM, ipady=5)

# Editando ligações
root.bind('<Control-Key-X>',cut_text)
root.bind('<Control-Key-C>',copy_text)
root.bind('<Control-Key-V>',paste_text)


root.mainloop()
