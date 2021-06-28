from tkinter import *
from tkinter import ttk
from telas import inclusao, listagem, resumo_autores, estatistica

def abre_inclusao():
  remove_frames()
  frame = inclusao.monta_formulario(root)
  frame.grid(row=1, column=1, sticky=W)

def abre_listagem():
  remove_frames()
  frame = listagem.monta_grid(root)
  frame.grid(row=1, column=1, sticky=W)

def abre_resumo():
  remove_frames()
  frame = resumo_autores.monta_grid_autores(root)
  frame.grid(row=1, column=1, sticky=W)

def abre_estatistica():
  remove_frames()
  frame = estatistica.monta_labels(root)
  frame.grid(row=1, column=1, sticky=W)

def remove_frames():
  for child in root.winfo_children(): 
    if str(child) != '.!menu':
      child.destroy()

root = Tk()
root.geometry('680x600+60+60')
root.title('Controle de Livros')

icon = PhotoImage(file = 'fotos/livraria2.png') 
root.iconphoto(False, icon)

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Inclusão", command=abre_inclusao)
filemenu.add_command(label="Listagem/Manutenção", command=abre_listagem)
filemenu.add_command(label="Resumo por Autores", command=abre_resumo)
filemenu.add_command(label="Estatística", command=abre_estatistica)
filemenu.add_separator()
filemenu.add_command(label="Sair", command=root.quit)
menubar.add_cascade(label="Cadastros", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Localizar")
helpmenu.add_command(label="Sobre...")
menubar.add_cascade(label="Ajuda", menu=helpmenu)

root.config(menu=menubar)
root.mainloop()