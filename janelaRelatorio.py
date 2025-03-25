import customtkinter as ctk
from customtkinter import CTkImage
import sqlite3 as sql
from pandas import DataFrame
from tkinter import messagebox, filedialog
from PIL import Image
from os import getlogin

usu = getlogin()

def abrirRelatorio():
    jRelatorio = ctk.CTk()
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
            conec = sql.connect(f'C:/Users/{usu}/AppData/Dados.db')
            cursor = conec.cursor()
            cursor.execute('Select DATA, COMPRAS, VALORES from compras')
            dados = cursor.fetchall()
            # Obtem os dados das colunas
            nome_Colunas = [descricao[0] for descricao in cursor.description]
            # Cria um df com pandas
            df = DataFrame(dados, columns=nome_Colunas)
            #Se der certo ele acha a pasta, se der errado ele grava no desktop
            try:
                if entryDir.get():
                    df.to_excel(f'{entryDir.get()}', index=False)
                    messagebox.showinfo('Planilha', 'Planilha gerada com sucesso.')
                else:
                    df.to_excel(f'C:/Users{usu}/Desktop/Planilha_Gastos.xlsx', index=False)
                    messagebox.showinfo('Planilha', 'Planilha gerada com sucesso.')
            finally:
                cursor.close()
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
        diretorio = filedialog.asksaveasfilename(
            initialdir='C:/Users/Desktop',
            initialfile='Planilha_Gastos.xlsx',
            defaultextension='xlsx',
            filetypes=[('Arquivos Excel', '*.xlsx')],
        )
        entryDir.delete(0, 'end')
        entryDir.insert(0, diretorio)

    entryDir = ctk.CTkEntry(jRelatorio,font=('Arial',17),height=30,width=380)
    entryDir.insert(0, f'C:/Users/{usu}/Desktop/Planilha_Gastos.xlsx') #Pode colocar uma variável que escolhe o padrão
    entryDir.place(x=65, y=19)
    #ctk.CTkButton(jRelatorio,text='',width=35,command=buscaDir,image=imgTkArquivo,fg_color='transparent').place(x=10,y=10)

    jRelatorio.mainloop()

