from janelaRelatorio import abrirRelatorio
from tkinter import messagebox
import customtkinter as ctk
from datetime import datetime
import sqlite3 as sql
from os import getlogin

usuario = getlogin()

def conectarSQLite():
    try:
        vaData = entryData.get()
        vaCompra = entryCompra.get()
        vaValor = entryValor.get()
        conexao = sql.connect(f'C:/Users/{usuario}/AppData/Dados.db')
        cursor = conexao.cursor()
        cursor.execute('''create table if not exists compras(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       DATA date not null,
                       COMPRAS text, 
                       VALORES text
                       )''')

        cursor.execute("insert into compras(DATA, COMPRAS, VALORES) values (?, ?, ?)", (vaData, vaCompra, vaValor))
        conexao.commit()
        cursor.close()
        conexao.close()
    except:
        pass

def inserirDados():
    vData = entryData.get()
    vCompra = entryCompra.get()
    vValor = entryValor.get()

    if not vData or not vCompra or not vValor:
        messagebox.showerror('ERRO', 'Insira todos os dados')
    else:
        try:
            float(vValor)
            dSalvar = messagebox.askyesno('SALVAR', 'DESEJA SALVAR?')
            if dSalvar:
                try:
                    conectarSQLite()
                    entryValor.delete(0, 'end')
                    entryCompra.delete(0, 'end')
                    messagebox.showinfo('CONCLUÍDO', 'DADOS SALVOS')
                except:
                    messagebox.showerror('ERRO', 'Falha ao salvar dados.')
            elif dSalvar:
                entryValor.delete(0, 'end')
                entryCompra.delete(0, 'end')
                messagebox.showerror('Cancelado', 'Operação Cancelada')
        except:
            messagebox.showerror('ERRO', 'Insira um valor válido!')



ctk.set_appearance_mode('System')
janela = ctk.CTk()
janela.title('Sistema de Gerenciamento de Gastos')
larguraTela = janela.winfo_screenwidth()
alturaTela = janela.winfo_screenheight()
larguraJanela = 300
alturaJanela = 230
x = (larguraTela-larguraJanela)//2
y = (alturaTela-alturaJanela)//2
janela.geometry(f'{larguraJanela}x{alturaJanela}+{x}+{y}')
janela.resizable(False, False)


lblData = ctk.CTkLabel(janela, text="Data:", font=('Arial', 17)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
entryData = ctk.CTkEntry(janela, font=('Arial', 15))
entryData.grid(row=0, column=1, pady=10)
entryData.insert(0, datetime.now().strftime('%d-%m-%Y'))

lblCompra = ctk.CTkLabel(janela, text='Compra:',font=('Arial', 17)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
entryCompra = ctk.CTkEntry(janela, font=('Arial', 15))
entryCompra.grid(row=1, column=1, pady=10)

lblValor = ctk.CTkLabel(janela, text='Valor:',font=('Arial', 17)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
entryValor = ctk.CTkEntry(janela, placeholder_text='R$',font=('Arial', 15))
entryValor.grid(row=2, column=1, pady=10)

btnGuardar = ctk.CTkButton(janela, text='GUARDAR', font=('Arial', 15), command=inserirDados, width=35, border_color='darkgrey').grid(row=3, column=0, padx=10, pady=10, sticky="w")

btnGerarRelatorio = ctk.CTkButton(janela, text='RELATÓRIO', font=('Arial', 15), width=35, border_color='darkgrey', command=abrirRelatorio).grid(row=3, column=1, padx=10, pady=10, sticky="w")

janela.mainloop()