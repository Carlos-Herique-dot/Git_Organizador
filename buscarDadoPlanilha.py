import sqlite3 as sql
from os import getlogin
from datetime import datetime

usu = getlogin()

def busDadosData():
    try:
        dados = sql.connect(f'C:/Users/{usu}/AppData/Dados.db')
        cursor = dados.cursor()
        comando = f"select compras, valores from compras where data = '{datetime.now().strftime('%d-%m-%Y')}'"
        cursor.execute(comando)
        resultados = cursor.fetchall()
        cursor.close()
        dados.close()
        return resultados
    except:
        print('ERRO')

busDadosData()



