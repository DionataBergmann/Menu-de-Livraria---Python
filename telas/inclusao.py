from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
import requests

URL_LIVROS = "http://localhost:3000/livros"

URL_AUTORES = "http://localhost:3000/autores"
r = requests.get(url=URL_AUTORES)
autores = r.json()

lista = []

for autor in autores:
  lista.append(autor["nome"])
autor_id = 0

def monta_formulario(notebook):

  def autor_selecionado(*args):
    global autor_id
    current_value = autores_cb.get()
    for autor in autores:
      if autor["nome"] == current_value:
        autor_id = autor["id"]    

  def incluir():
    dados = {"titulo": titulo.get(),
             "autor_id": autor_id,
             "ano": ano.get(),
             "preco": preco.get(),
             "foto": foto.get()}

    response = requests.post(URL_LIVROS, json=dados)

    if response.status_code == 201:
      showinfo(title='Livro Cadastrado',
             message=f"Código do Livro {response.text}")
    else:
      showinfo(title='Erro...',
               message="Livro não cadastrado")

  cadframe = ttk.Frame(notebook, width=680, height=580)

  ttk.Label(cadframe, text="Titulo: ").grid(column=1, row=1, sticky=E)
  ttk.Label(cadframe, text="Autor: ").grid(column=1, row=2, sticky=E)
  ttk.Label(cadframe, text="Ano: ").grid(column=1, row=3, sticky=E)
  ttk.Label(cadframe, text="Preço R$: ").grid(column=1, row=4, sticky=E)
  ttk.Label(cadframe, text="URL da Foto: ").grid(column=1, row=5, sticky=E)

  titulo = StringVar()
  titulo_entry = ttk.Entry(cadframe, width=40, textvariable=titulo)
  titulo_entry.grid(column=2, row=1, sticky=W)

  autores_cb = ttk.Combobox(cadframe)
  autores_cb["values"] = lista
  autores_cb.grid(column=2, row=2, sticky=W)
  autores_cb.bind('<<ComboboxSelected>>', autor_selecionado)

  ano = StringVar()
  ttk.Entry(cadframe, width=10, textvariable=ano).grid(column=2, row=3, sticky=W)

  preco = StringVar()
  ttk.Entry(cadframe, width=20, textvariable=preco).grid(column=2, row=4, sticky=W)

  foto = StringVar()
  ttk.Entry(cadframe, width=60, textvariable=foto).grid(column=2, row=5, sticky=W)

  ttk.Button(cadframe, text="Incluir Livro", command=incluir).grid(column=2, row=6, sticky=W)

  for child in cadframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

  return cadframe