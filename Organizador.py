import tkinter

from buscarDadoPlanilha import busDadosData
from customtkinter import CTkImage
from pandas import DataFrame
from tkinter import messagebox, filedialog, ttk
import customtkinter as ctk
from datetime import datetime
import sqlite3 as sql
from PIL import Image
from os import getlogin

usuario = getlogin()
ctk.set_appearance_mode('System')
janela = ctk.CTk()

'''def treeDados():
    tree = ttk.Treeview(janela, columns=('compras', 'valores'), show='headings')
    tree.heading('compras', text='COMPRAS')
    tree.heading('valores', text='VALORES')
    tree.place(x=10, y=250)
    for linha in busDadosData():
        tree.insert('', tkinter.END, values=linha)

    # Estilo da coluna
    style = ttk.Style()
    style.configure('Treeview.Heading', font=('Arial', 15))
    style.configure('Treeview', rowheight=25, font=('Arial', 15), background="grey")
    tree.column('compras', width=200)
    tree.column('valores', width=155)
'''

def mostrarDados():
    for linha in busDadosData():
        print(linha[0], linha[1])
        txtDados.insert('end', f'{linha[0]:<45}R$ {float(linha[1]):.2f}' +'\n')
        txtDados.place(x=10, y=190)
txtDados = ctk.CTkTextbox(janela, height=200, width=250)

def atualizaMostraDados():
    txtDados.delete('0.0', 'end')
mostrarDados()

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
                    atualizaMostraDados()
                    mostrarDados()
                except:
                    messagebox.showerror('ERRO', 'Falha ao salvar dados.')
            elif dSalvar:
                entryValor.delete(0, 'end')
                entryCompra.delete(0, 'end')
                messagebox.showerror('Cancelado', 'Operação Cancelada')
        except:
            messagebox.showerror('ERRO', 'Insira um valor válido!')


def abrirRelatorio():
    janela.withdraw()
    jRelatorio = ctk.CTkToplevel(janela)
    jRelatorio.title('Relatório')
    larguraTelaR = jRelatorio.winfo_screenwidth()
    alturaTelaR = jRelatorio.winfo_screenheight()
    larguraJanelaR = 450
    alturaJanelaR = 200
    xR = (larguraTelaR - larguraJanelaR) //2
    yR = (alturaTelaR - alturaJanelaR) // 2
    jRelatorio.geometry(f'{larguraJanelaR}x{alturaJanelaR}+{xR}+{yR}')
    jRelatorio.resizable(False, False)

#Botao que cria o arquivo Excel
    def criarExcel():
        try:
            # Conecta no BD e puxa as informações
            conec = sql.connect(f'C:/Users/{usuario}/AppData/Dados.db')
            cursor = conec.cursor()
            cursor.execute('Select DATA, COMPRAS, VALORES from compras')
            dados = cursor.fetchall()
            # Obtem os dados das colunas
            nome_Colunas = [descricao[0] for descricao in cursor.description]
            # Cria um df com pandas
            df = DataFrame(dados, columns=nome_Colunas)
            #Se der certo ele acha a pasta, se der errado ele grava no desktop
            try:
                df.to_excel(f'{entryDir.get()}/Gastos.xlsx', index=False)
            except:
                df.to_excel(f'C:/Users/{usuario}/Desktop/Gastos.xlsx', index=False)
            messagebox.showinfo('Planilha', 'Planilha gerada com sucesso.')
            conec.close()
        except:
            messagebox.showerror('ERRO', 'Erro ao gerar relatório.')

    imgEx = Image.open('excel.png')
    imgExTk = CTkImage(light_image=imgEx, dark_image=imgEx, size=(35,35))
    ctk.CTkButton(jRelatorio, text='',image=imgExTk, width=35, font=('Arial', 17), fg_color='transparent', command=criarExcel).place(x=25, y=100)

    #Cria o botão que abrirá o diretório com uma imagem de ícone
    imgArquivo = Image.open('arquivo.png')
    imgTkArquivo = CTkImage(light_image=imgArquivo, dark_image=imgArquivo, size=(35,35))

    def buscaDir():
        diretorio = filedialog.askdirectory()
        entryDir.configure(state='normal')
        entryDir.delete(0, 'end')
        entryDir.insert(0, diretorio)

    entryDir = ctk.CTkEntry(jRelatorio,font=('Arial',17),height=30,width=380)
    entryDir.insert(0, f'C:/Users/Desktop/{usuario}/Gastos.xlsx')
    entryDir.configure(state='disabled')
    entryDir.place(x=60, y=15)
    ctk.CTkButton(jRelatorio,text='',width=35,command=buscaDir,image=imgTkArquivo,fg_color='transparent').place(x=10,y=10)

    def abrirJanela():
        janela.deiconify()
        jRelatorio.destroy()
    jRelatorio.protocol('WM_DELETE_WINDOW', abrirJanela)

#Configurações da página

janela.title('Sistema de Gerenciamento de Gastos')
larguraTela = janela.winfo_screenwidth()
alturaTela = janela.winfo_screenheight()
larguraJanela = 270
alturaJanela = 400
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