from tkinter import *
from tkinter import ttk
import requests

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') 

num = 0
total = 0
maior = 0
menor = 0
livros_maiores = []
livros_menores = []
destaques = 0
livros = None

def dados():
  global num, total, maior, menor, destaques, livros, livros_maiores, livros_menores

  num = 0
  total = 0
  maior = 0
  menor = 1000
  livros_maiores = []
  livros_menores = []
  destaques = 0

  URL_LIVROS = "http://localhost:3000/livros"
  r = requests.get(url=URL_LIVROS)
  livros = r.json()

  for livro in livros:
    num += 1
    total += float(livro["preco"])
    if float(livro["preco"]) > maior:
      maior = float(livro["preco"])  
    if float(livro["preco"]) < menor:
      menor = float(livro["preco"])   
    if livro["destaque"]:
      destaques += 1  

  for livro in livros:
    if float(livro["preco"]) == maior:
      livros_maiores.append(livro["titulo"])
    if float(livro["preco"]) == menor:
      livros_menores.append(livro["titulo"])

def monta_labels(notebook):

  cadframe = ttk.Frame(notebook, width=680, height=580)

  dados()

  totalf = locale.currency(total, grouping=True, symbol=None)
  media = total / num
  mediaf = locale.currency(media, grouping=True, symbol=None)
  maiorf = locale.currency(maior, grouping=True, symbol=None)
  menorf = locale.currency(menor, grouping=True, symbol=None)

  ttk.Label(cadframe, text=f"Número de livros Cadastrados: {num}").grid(column=1, row=1, sticky=W)
  ttk.Label(cadframe, text=f"Número de livros em Destaque: {destaques}").grid(column=1, row=2, sticky=W)
  ttk.Label(cadframe, text=f"Total do Preço dos livros R$: {totalf}").grid(column=1, row=3, sticky=W)
  ttk.Label(cadframe, text=f"Preço Médio dos livros R$: {mediaf}").grid(column=1, row=4, sticky=W)
  ttk.Label(cadframe, text=f"Maior Preço de livros R$: {maiorf}").grid(column=1, row=5, sticky=W)
  ttk.Label(cadframe, text=f"Menor Preço de livros R$: {menorf}").grid(column=1, row=6, sticky=W)
  ttk.Label(cadframe, text=f"Livro(s) de Maior Preço: {', '.join(livros_maiores)}").grid(column=1, row=7, sticky=W)
  ttk.Label(cadframe, text=f"Livro(s) de Menor Preço: {', '.join(livros_menores)}").grid(column=1, row=8, sticky=W)

  for child in cadframe.winfo_children(): 
    child.grid_configure(padx=20, pady=10)    

  return cadframe