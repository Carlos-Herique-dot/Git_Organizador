import pandas as pd
from tkinter import messagebox
import customtkinter as ctk
from datetime import datetime
import sqlite3 as sql

def conectarSQLite():
    vaData = entryData.get()
    vaCompra = entryCompra.get()
    vaValor = entryValor.get()
    try:
        conexao = sql.connect('Dados.db')
        cursor = conexao.cursor()
        cursor.execute('''create table if not exists compras(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       DATA date not null,
                       COMPRAS text, 
                       VALORES text
                       )''')

        cursor.execute("insert into compras(DATA, COMPRAS, VALORES) values (?, ?, ?)", (vaData, vaCompra, vaValor))
        conexao.commit()
        conexao.close()
        #print('Sucesso')
    except:
        print('Erro ao conectar SQLite')

def inserirDados():
    vData = entryData.get()
    vCompra = entryCompra.get()
    vValor = entryValor.get()

    if not vData or not vCompra or not vValor:
        messagebox.showerror('ERRO', 'Insira todos os dados')
    else:
        dSalvar = messagebox.askyesno('SALVAR', 'DESEJA SALVAR?')
        if dSalvar == True:
            conectarSQLite()
            entryValor.delete(0, 'end')
            entryCompra.delete(0,'end')
            messagebox.showinfo('CONCLUÍDO', 'DADOS SALVO')
        elif dSalvar == False:
            entryValor.delete(0, 'end')
            entryCompra.delete(0, 'end')
            vValor=''
            vCompra=''
            vData=''
            messagebox.showerror('Cancelado', 'Operação Cancelada')

def criarExcel():
    try:
        #Conecta no BD e puxa as informações
        conec = sql.connect('Dados.db')
        cursor = conec.cursor()
        cursor.execute('Select DATA, COMPRAS, VALORES from compras')
        dados = cursor.fetchall()
        print('Conectou')
        #Obtem os dados das colunas
        nome_Colunas = [descricao[0] for descricao in cursor.description]
        print('Leu as colunas')
        #Cria um df com pandas
        df = pd.DataFrame(dados, columns=nome_Colunas)
        df.to_excel('Gastos.xlsx', index=False)
        print('Gerou o excel')
        messagebox.showinfo('Planilha', 'Planilha gerada com sucesso.')
        conec.close()

    except:
        messagebox.showerror('ERRO', 'Erro ao gerar relatório.')

def abrirRelatorio():
    jRelatorio = ctk.CTkToplevel(janela)
    jRelatorio.title('Relatório')
    larguraTelaR = jRelatorio.winfo_screenwidth()
    alturaTelaR = jRelatorio.winfo_screenheight()
    larguraJanelaR = 250
    alturaJanelaR = 200
    xR = (larguraTelaR - larguraJanelaR) -100
    yR = (alturaTelaR - alturaJanelaR) // 2
    jRelatorio.geometry(f'{larguraJanelaR}x{alturaJanelaR}+{xR}+{yR}')
    jRelatorio.resizable(False, False)

    lblCriarEx = ctk.CTkButton(jRelatorio, text='Planilha', width=35, font=('Arial', 17), command=criarExcel).place(x=25, y=25)



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