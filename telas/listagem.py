from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, askyesno
import requests

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') 

URL_LIVROS = "http://localhost:3000/livros"
livros = None

def atualiza_lista():
  global livros
  r = requests.get(url=URL_LIVROS)
  livros = r.json()

def preenche_grid(tree):
  for livro in livros:
    precof = locale.currency(float(livro["preco"]), grouping=True, symbol=None)
    destaque = "★" if livro["destaque"] else ""
    tree.insert('', END, values=(livro["id"], livro["titulo"], livro["autor"], livro["ano"], precof, destaque));

def monta_grid(notebook):
  atualiza_lista()
  gridframe = ttk.Frame(notebook, width=680, height=580)

  columns = ('#1', '#2', '#3', '#4', "#5", "#6")

  tree = ttk.Treeview(gridframe, columns=columns, show='headings')

  tree.heading('#1', text='Código')
  tree.heading('#2', text='titulo')
  tree.heading('#3', text='Autor')
  tree.heading('#4', text='Ano')
  tree.heading('#5', text='Preço R$')
  tree.heading('#6', text='Destaques')

  tree.column("#1", width=50, anchor=CENTER)
  tree.column("#2", width=200)
  tree.column("#3", width=100)
  tree.column("#4", width=60, anchor=CENTER)
  tree.column("#5", width=100, anchor=E)
  tree.column("#6", width=60, anchor=CENTER)

  preenche_grid(tree)

  # bind the select event
  def item_selected(event):
    selected = tree.focus()
    temp = tree.item(selected, 'values')

    if temp[5]:
      answer = askyesno(title='Confirmação',
                        message='Deseja Retirar do Destaque Este Livro?')
      if answer:
        requests.put(url=URL_LIVROS+"/destaque/"+str(temp[0]))
        tree.item(selected, values=(temp[0], temp[1], temp[2], temp[3], temp[4], ""))        
        atualiza_lista()
    else:
      answer = askyesno(title='Confirmação',
                     message='Deseja Destacar Este Livro?')
      if answer:
        requests.put(url=URL_LIVROS+"/destaque/"+str(temp[0]))
        tree.item(selected, values=(temp[0], temp[1], temp[2], temp[3], temp[4], "★"))
        atualiza_lista()

  tree.bind('<<TreeviewSelect>>', item_selected)

  tree.grid(row=1, column=0, sticky='nsew', padx=(10, 0), pady=10)

  # add a scrollbar
  scrollbar = ttk.Scrollbar(gridframe, orient=VERTICAL, command=tree.yview)
  tree.configure(yscroll=scrollbar.set)
  scrollbar.grid(row=1, column=1, sticky='ns')

  filter_order_frame = ttk.Frame(gridframe)
  filter_order_frame.grid(row=2, column=0, columnspan=2, pady=12)

  filterframe = ttk.Frame(filter_order_frame)
  filterframe.grid(row=0, column=0, padx=(10, 20))

  preco = StringVar()

  def limpa():
    for i in tree.get_children():
      tree.delete(i)

  def exibir_todos():
    limpa()
    preenche_grid(tree)
    preco.set("")  

  def filtro():
    ttk.Label(filterframe, text="Limite de Preço: ").grid(column=0, row=1, sticky=W)
    ttk.Entry(filterframe, width=20, textvariable=preco).grid(column=0, row=2, sticky=W)

    def filtrar():
      limpa()
      for livro in livros:
        if (float(livro["preco"]) <= float(preco.get())):
          precof = locale.currency(float(livro["preco"]), grouping=True, symbol=None)
          destaque = "★" if livro["destaque"] else ""
          tree.insert('', END, values=(livro["id"], livro["titulo"], livro["autor"], livro["ano"], precof, destaque))

      if len(tree.get_children()) == 0:
        showinfo(title="Atenção",
                message=f"Não há livros com preço inferior a {preco.get()}")
        exibir_todos()        

    ttk.Button(filterframe, text="Filtar", command=filtrar).grid(column=1, row=2, sticky=W)    
    ttk.Button(filterframe, text="Todos", command=exibir_todos).grid(column=2, row=2, sticky=W)

  filtro()

  orderframe = ttk.Frame(filter_order_frame)
  orderframe.grid(row=0, column=1)

  def ordem():
    ttk.Label(orderframe, text="Selecione a ordem desejada").grid(column=0, columnspan=3, row=0, sticky=W)

    order = StringVar()
    order.set("id")
    ttk.Radiobutton(orderframe, text='Código', variable=order, value='id').grid(column=0, row=1, sticky=W)
    ttk.Radiobutton(orderframe, text='Titulo', variable=order, value='titulo').grid(column=1, row=1, sticky=W)
    ttk.Radiobutton(orderframe, text='Ano', variable=order, value='ano').grid(column=2, row=1, sticky=W)
    
    def ordenar():
      global livros
      if order.get() == "id":
        livros = sorted(livros, key=lambda book: book['id'], reverse=True) 
      elif order.get() == "titulo":
        livros = sorted(livros, key=lambda book: book['titulo']) 
      elif order.get() == "ano":  
        livros = sorted(livros, key=lambda book: book['ano']) 

      exibir_todos()

    ttk.Button(orderframe, text="Ordenar", command=ordenar).grid(column=3, row=1, sticky=W)

  ordem()

  return gridframe