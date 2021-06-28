from tkinter import *
from tkinter import ttk
import requests

URL_LIVROS = "http://localhost:3000/livros"

autores = {}
livros = {}

def agrupa_autores():
  global livros, autores
  autores = {}
  r = requests.get(url=URL_LIVROS)
  livros = r.json()
  for livro in livros:
    if livro["autor"] in autores:
      autores[livro["autor"]] += 1
    else:
      autores[livro["autor"]] = 1  

def preenche_grid_autores(tree):
  agrupa_autores()
  # adding data to the treeview
  for autor, num in autores.items():
    tree.insert('', END, values=(autor, num))

def monta_grid_autores(notebook):
  gridframe = ttk.Frame(notebook, width=250, height=580)

  # columns
  columns = ('#1', '#2')

  tree = ttk.Treeview(gridframe, columns=columns, show='headings')

  # define headings
  tree.heading('#1', text='Autor')
  tree.heading('#2', text='Nº Livros')

  # largura de cada coluna
  tree.column("#1", width=150)
  tree.column("#2", width=100, anchor=CENTER)

  preenche_grid_autores(tree)

  # bind the select event
  def item_selected(event):
    selected = tree.focus()
    temp = tree.item(selected, 'values')

  tree.bind('<<TreeviewSelect>>', item_selected)

  tree.grid(row=1, column=0, sticky='nsew', padx=(10, 0), pady=10)

  # add a scrollbar
  scrollbar = ttk.Scrollbar(gridframe, orient=VERTICAL, command=tree.yview)
  tree.configure(yscroll=scrollbar.set)
  scrollbar.grid(row=1, column=1, sticky='ns')

  return gridframe