import sqlite3 as sql
from os import getlogin

usu = getlogin()
def busDadosData(date):
    dados = sql.connect(f'C:/Users/{usu}/AppData/Dados.db')
    cursor = dados.cursor()

    comando = f"select * from compras where data = '{date}'"
    cursor.execute(comando)
    resultados = cursor.fetchall()

    print(resultados)

    cursor.close()
    dados.close()


